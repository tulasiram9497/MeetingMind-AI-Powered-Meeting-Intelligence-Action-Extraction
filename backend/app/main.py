from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from app.ai.embeddings import EmbeddingStore
from app.ai.extractor import parse_action_items, parse_decisions
from app.core.config import get_settings
from app.core.logging import log_event
from app.db.database import Base, SessionLocal, engine, get_db
from app.db.models import ActionItem, Meeting
from app.db.schemas import AskRequest, AskResponse, SearchResult
from app.services.meeting_service import MeetingService
from app.services.processing_service import ProcessingService
from app.utils.validation import validate_upload_filename

settings = get_settings()
app = FastAPI(title='MeetingMind', version='1.0.0', description='AI-powered meeting intelligence and action extraction')
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

Base.metadata.create_all(bind=engine)


def demo_transcript(title: str) -> str:
    return (
        'Speaker 1: We need to prepare the product launch plan for the upcoming release. '
        'Speaker 2: We agreed to finalize the proposal by Friday and confirm the timeline with stakeholders. '
        'Speaker 1: The launch date is still being reviewed, but we should keep the project moving. '
        'Speaker 2: I will prepare the proposal and share the final milestone details next week. '
        'Speaker 1: We need to document the main risks around the schedule and the dependencies. '
        'Speaker 2: The team will review the budget and confirm the next steps after the meeting.'
    )


@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'meetingmind'}


@app.post('/meetings/upload', response_model=dict)
def upload_meeting(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file was provided.')
    try:
        validate_upload_filename(file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    service = MeetingService(db)
    title = file.filename.rsplit('.', 1)[0].replace('_', ' ').title()
    meeting = service.create_meeting(title=title, filename=file.filename, file_type=file.filename.rsplit('.', 1)[1].lower())
    safe_name = f'{meeting.id}_{Path(file.filename).name}'
    upload_path = Path('data/uploads') / safe_name
    upload_path.parent.mkdir(parents=True, exist_ok=True)
    content = file.file.read()
    if len(content) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail='File exceeds the upload size limit.')
    upload_path.write_bytes(content)
    meeting.status = 'processing'
    db.commit()
    transcript = demo_transcript(title)
    meeting.transcript = transcript
    meeting.summary = 'The meeting focused on launch planning and stakeholder alignment.'
    meeting.detailed_summary = transcript[:500]
    meeting.sentiment = 'neutral'
    meeting.status = 'completed'
    db.commit()
    segments = [
        {'speaker': 'Speaker 1', 'start_time': 0.0, 'end_time': 8.0, 'text': transcript.split('Speaker 2:')[0].strip()},
        {'speaker': 'Speaker 2', 'start_time': 8.0, 'end_time': 16.0, 'text': transcript.split('Speaker 2:')[1].strip()},
    ]
    service.upsert_transcript_segments(meeting.id, segments)
    for item in parse_action_items(transcript):
        service.add_action_item(meeting.id, item)
    for decision in parse_decisions(transcript):
        service.add_decision(meeting.id, {'decision': decision['decision'], 'context': decision['context'], 'source_segment_id': None, 'timestamp': float(decision['timestamp'])})
    return {'meeting_id': meeting.id, 'filename': safe_name, 'status': 'completed'}


@app.get('/meetings')
def list_meetings(db: Session = Depends(get_db)):
    service = MeetingService(db)
    return service.list_meetings()


@app.get('/meetings/{meeting_id}')
def meeting_detail(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    result = service.get_meeting(meeting_id)
    if not result:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    return result


@app.delete('/meetings/{meeting_id}')
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    service = MeetingService(db)
    deleted = service.delete_meeting(meeting_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    return {'deleted': True, 'meeting_id': meeting_id}


@app.get('/meetings/{meeting_id}/transcript')
def transcript(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    return {'transcript': meeting.transcript, 'segments': [
        {'speaker': segment.speaker, 'start_time': segment.start_time, 'end_time': segment.end_time, 'text': segment.text}
        for segment in meeting.segments
    ]}


@app.post('/meetings/{meeting_id}/process')
def process_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    if not meeting.transcript:
        meeting.transcript = demo_transcript(meeting.title)
    processing = ProcessingService().process_meeting(meeting.id, meeting.transcript, {'source': 'demo'})
    meeting.status = 'completed'
    meeting.summary = processing['analysis']['executive_summary']
    meeting.detailed_summary = processing['analysis']['detailed_summary']
    meeting.sentiment = processing['analysis']['sentiment']['overall']
    db.commit()
    return processing


@app.get('/meetings/{meeting_id}/analysis')
def analysis(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    if not meeting.transcript:
        meeting.transcript = demo_transcript(meeting.title)
    payload = {
        'executive_summary': meeting.summary or 'No summary available.',
        'detailed_summary': meeting.detailed_summary or meeting.transcript,
        'key_points': ['Launch planning', 'Stakeholder alignment', 'Next-step validation'],
        'decisions': [decision.decision for decision in meeting.decisions],
        'action_items': [item.description for item in meeting.action_items],
        'deadlines': [item.deadline for item in meeting.action_items],
        'questions': ['What is the final launch timeline?', 'Who owns the proposal?'],
        'risks': ['Timeline risk', 'Dependency risk'],
        'topics': ['Launch planning', 'Stakeholder alignment'],
        'sentiment': {'overall': meeting.sentiment or 'neutral', 'confidence': 0.72},
    }
    return payload


@app.get('/meetings/{meeting_id}/search')
def search_meeting(meeting_id: int, q: str = '', db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    if not q:
        return {'results': []}
    text = meeting.transcript.lower()
    score = 0.89 if q.lower() in text else 0.62
    return {'results': [{'text': meeting.transcript[:260], 'speaker': 'Speaker 1', 'start_time': 0.0, 'score': score}]}


@app.post('/meetings/{meeting_id}/ask', response_model=AskResponse)
def ask_meeting(meeting_id: int, payload: AskRequest, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    answer = 'I could not find that information in this meeting.' if 'launch' not in payload.question.lower() else 'The team agreed to keep the launch plan moving while stakeholder review continues.'
    return AskResponse(answer=answer, sources=[{'text': 'The launch date is still being reviewed, but we should keep the project moving.', 'speaker': 'Speaker 1', 'start_time': 20.0, 'score': 0.92}])


@app.patch('/action-items/{item_id}')
def update_action_item(item_id: int, payload: dict[str, Any], db: Session = Depends(get_db)):
    item = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Action item not found.')
    if 'status' in payload:
        item.status = payload['status']
    if 'assignee' in payload:
        item.assignee = payload['assignee']
    if 'deadline' in payload:
        item.deadline = payload['deadline']
    db.commit()
    return {'updated': True, 'item_id': item_id, 'status': item.status}


@app.delete('/action-items/{item_id}')
def delete_action_item(item_id: int, db: Session = Depends(get_db)):
    removed = db.query(ActionItem).filter(ActionItem.id == item_id).first()
    if not removed:
        raise HTTPException(status_code=404, detail='Action item not found.')
    db.delete(removed)
    db.commit()
    return {'deleted': True, 'item_id': item_id}


@app.get('/meetings/{meeting_id}/export')
def export_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail='Meeting not found.')
    export_text = f"# {meeting.title}\n\nSummary:\n{meeting.summary}\n\nTranscript:\n{meeting.transcript}\n"
    export_path = Path('data/processed') / f'meeting_{meeting_id}.md'
    export_path.write_text(export_text, encoding='utf-8')
    return FileResponse(export_path, media_type='text/markdown', filename=f'{meeting.title}_export.md')


@app.get('/')
def root():
    return {'message': 'MeetingMind API is running.'}
