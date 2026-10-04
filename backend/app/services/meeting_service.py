from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.db.models import ActionItem, Decision, Meeting, Question, Topic, TranscriptSegment
from app.db.schemas import ActionItemSchema, DecisionSchema, MeetingDetailSchema, MeetingSchema, QuestionSchema, TopicSchema, TranscriptSegmentSchema


class MeetingService:
    def __init__(self, db: Session):
        self.db = db

    def create_meeting(self, title: str, filename: str, file_type: str, duration: float = 0.0) -> Meeting:
        meeting = Meeting(
            title=title,
            original_filename=filename,
            file_type=file_type,
            duration=duration,
            status='uploaded',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(meeting)
        self.db.commit()
        self.db.refresh(meeting)
        return meeting

    def list_meetings(self) -> list[MeetingSchema]:
        meetings = self.db.query(Meeting).order_by(Meeting.created_at.desc()).all()
        return [MeetingSchema.model_validate(meeting) for meeting in meetings]

    def get_meeting(self, meeting_id: int) -> MeetingDetailSchema | None:
        meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return None
        return MeetingDetailSchema(
            id=meeting.id,
            title=meeting.title,
            original_filename=meeting.original_filename,
            file_type=meeting.file_type,
            duration=meeting.duration,
            status=meeting.status,
            created_at=meeting.created_at,
            updated_at=meeting.updated_at,
            transcript=meeting.transcript,
            summary=meeting.summary,
            detailed_summary=meeting.detailed_summary,
            sentiment=meeting.sentiment,
            segments=[TranscriptSegmentSchema.model_validate(segment) for segment in meeting.segments],
            action_items=[ActionItemSchema.model_validate(item) for item in meeting.action_items],
            decisions=[DecisionSchema.model_validate(item) for item in meeting.decisions],
            topics=[TopicSchema.model_validate(item) for item in meeting.topics],
            questions=[QuestionSchema.model_validate(item) for item in meeting.questions],
        )

    def delete_meeting(self, meeting_id: int) -> bool:
        meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return False
        self.db.delete(meeting)
        self.db.commit()
        return True

    def upsert_transcript_segments(self, meeting_id: int, segments: list[dict[str, Any]]) -> None:
        for segment in segments:
            record = TranscriptSegment(
                meeting_id=meeting_id,
                speaker=segment.get('speaker', 'Speaker 1'),
                start_time=float(segment.get('start_time', 0.0)),
                end_time=float(segment.get('end_time', 0.0)),
                text=segment.get('text', ''),
            )
            self.db.add(record)
        self.db.commit()

    def add_action_item(self, meeting_id: int, item: dict[str, Any]) -> ActionItem:
        action_item = ActionItem(meeting_id=meeting_id, **item)
        self.db.add(action_item)
        self.db.commit()
        self.db.refresh(action_item)
        return action_item

    def add_decision(self, meeting_id: int, decision: dict[str, Any]) -> Decision:
        record = Decision(meeting_id=meeting_id, **decision)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def add_topic(self, meeting_id: int, topic: dict[str, str]) -> Topic:
        record = Topic(meeting_id=meeting_id, **topic)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def add_question(self, meeting_id: int, question: dict[str, Any]) -> Question:
        record = Question(meeting_id=meeting_id, **question)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_action_item_status(self, item_id: int, status: str) -> ActionItem | None:
        item = self.db.query(ActionItem).filter(ActionItem.id == item_id).first()
        if not item:
            return None
        item.status = status
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_action_item(self, item_id: int) -> bool:
        item = self.db.query(ActionItem).filter(ActionItem.id == item_id).first()
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
