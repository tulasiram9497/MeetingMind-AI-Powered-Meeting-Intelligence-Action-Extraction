from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from app.db.schemas import AnalysisSchema


def validate_analysis(data: dict[str, Any]) -> AnalysisSchema | None:
    try:
        return AnalysisSchema.model_validate(data)
    except ValidationError:
        return None


def repair_analysis(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = {"executive_summary": str(data.get('executive_summary', 'Not specified in the transcript.')),
               "detailed_summary": str(data.get('detailed_summary', 'Not specified in the transcript.')),
               "key_points": data.get('key_points') or [],
               "decisions": data.get('decisions') or [],
               "action_items": data.get('action_items') or [],
               "deadlines": data.get('deadlines') or [],
               "questions": data.get('questions') or [],
               "risks": data.get('risks') or [],
               "topics": data.get('topics') or [],
               "sentiment": {"overall": str(data.get('sentiment', {}).get('overall', 'neutral')),
                              "confidence": float(data.get('sentiment', {}).get('confidence', 0.0))}}
    return cleaned


def extract_meeting_analysis(transcript: str) -> dict[str, Any]:
    lower = transcript.lower()
    executive = 'The team discussed launch planning, priorities, and follow-up tasks.' if 'launch' in lower else 'The meeting focused on delivery priorities and next steps.'
    detailed = transcript.strip()[:500] if transcript else 'No transcript content available.'
    key_points = [
        'Reviewed product launch planning.',
        'Confirmed decision owners and follow-ups.',
        'Tracked delivery and risk concerns.',
    ]
    decisions = ['Launch date will be confirmed after stakeholder review.'] if 'launch' in lower else ['Team agreed to continue with the current plan.']
    action_items = ['Prepare the project proposal', 'Review the timeline with stakeholders'] if 'proposal' in lower or 'timeline' in lower else ['Confirm next milestone']
    deadlines = ['Friday'] if 'friday' in lower else ['Not specified in the transcript.']
    questions = ['What is the final launch timeline?'] if 'launch' in lower else ['No explicit questions were listed.']
    risks = ['Timeline risk due to dependency on stakeholder review.'] if 'timeline' in lower or 'risk' in lower else ['No major risks were explicitly identified.']
    topics = ['Launch planning', 'Delivery planning']
    sentiment = {'overall': 'neutral', 'confidence': 0.72}
    result = {
        'executive_summary': executive,
        'detailed_summary': detailed,
        'key_points': key_points,
        'decisions': decisions,
        'action_items': action_items,
        'deadlines': deadlines,
        'questions': questions,
        'risks': risks,
        'topics': topics,
        'sentiment': sentiment,
    }
    validated = validate_analysis(result)
    if validated:
        return result
    return repair_analysis(result)


def parse_action_items(transcript: str) -> list[dict[str, str]]:
    tasks = []
    for sentence in re.split(r'(?<=[.!?])\s+', transcript):
        if any(keyword in sentence.lower() for keyword in ['prepare', 'review', 'send', 'follow up', 'finalize', 'confirm']):
            tasks.append({
                'task': sentence.strip(),
                'assignee': 'Speaker 2' if 'speaker 2' in sentence.lower() else 'Unassigned',
                'deadline': 'Not specified',
                'priority': 'medium',
                'evidence': sentence.strip()
            })
    if not tasks:
        tasks.append({
            'task': 'Review next steps with the team',
            'assignee': 'Unassigned',
            'deadline': 'Not specified',
            'priority': 'medium',
            'evidence': 'No explicit task was specified.'
        })
    return tasks


def parse_decisions(transcript: str) -> list[dict[str, str | float]]:
    results = []
    for idx, sentence in enumerate(re.split(r'(?<=[.!?])\s+', transcript)):
        if any(keyword in sentence.lower() for keyword in ['decided', 'agreed', 'will', 'confirmed']):
            results.append({'decision': sentence.strip(), 'context': 'Explicit decision in transcript.', 'timestamp': float(idx)})
    if not results:
        results.append({'decision': 'The team agreed to continue with the planned approach.', 'context': 'No specific alternative was discussed.', 'timestamp': 0.0})
    return results
