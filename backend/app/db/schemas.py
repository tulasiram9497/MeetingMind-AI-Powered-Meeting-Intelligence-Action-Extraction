from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


class TranscriptSegmentSchema(BaseModel):
    id: int | None = None
    speaker: str = 'Speaker 1'
    start_time: float = 0.0
    end_time: float = 0.0
    text: str


class ActionItemSchema(BaseModel):
    id: int | None = None
    description: str
    assignee: str = 'Unassigned'
    deadline: str = 'Not specified'
    priority: Literal['low', 'medium', 'high'] = 'medium'
    status: Literal['open', 'in_progress', 'completed'] = 'open'
    source_segment_id: int | None = None


class DecisionSchema(BaseModel):
    id: int | None = None
    decision: str
    context: str = ''
    source_segment_id: int | None = None
    timestamp: float = 0.0


class TopicSchema(BaseModel):
    id: int | None = None
    name: str
    description: str = ''


class QuestionSchema(BaseModel):
    id: int | None = None
    question: str
    answer: str = ''
    source_segment_id: int | None = None


class SentimentSchema(BaseModel):
    overall: str = 'neutral'
    confidence: float = 0.0


class AnalysisSchema(BaseModel):
    executive_summary: str = ''
    detailed_summary: str = ''
    key_points: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list)
    deadlines: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    sentiment: SentimentSchema = SentimentSchema()


class MeetingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = None
    title: str
    original_filename: str
    file_type: str
    duration: float = 0.0
    status: str = 'uploaded'
    created_at: datetime | None = None
    updated_at: datetime | None = None
    transcript: str = ''
    summary: str = ''
    detailed_summary: str = ''
    sentiment: str = 'neutral'


class MeetingDetailSchema(MeetingSchema):
    segments: list[TranscriptSegmentSchema] = Field(default_factory=list)
    action_items: list[ActionItemSchema] = Field(default_factory=list)
    decisions: list[DecisionSchema] = Field(default_factory=list)
    topics: list[TopicSchema] = Field(default_factory=list)
    questions: list[QuestionSchema] = Field(default_factory=list)


class UploadResponse(BaseModel):
    meeting_id: int
    filename: str
    status: str


class AskRequest(BaseModel):
    question: str


class SearchResult(BaseModel):
    text: str
    speaker: str = 'Speaker 1'
    start_time: float = 0.0
    score: float = 0.0


class AskResponse(BaseModel):
    answer: str
    sources: list[SearchResult] = Field(default_factory=list)
