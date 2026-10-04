from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    duration = Column(Float, default=0.0)
    status = Column(String(50), default='uploaded')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transcript = Column(Text, default='')
    summary = Column(Text, default='')
    detailed_summary = Column(Text, default='')
    sentiment = Column(String(255), default='neutral')

    segments = relationship('TranscriptSegment', back_populates='meeting', cascade='all, delete-orphan')
    action_items = relationship('ActionItem', back_populates='meeting', cascade='all, delete-orphan')
    decisions = relationship('Decision', back_populates='meeting', cascade='all, delete-orphan')
    topics = relationship('Topic', back_populates='meeting', cascade='all, delete-orphan')
    questions = relationship('Question', back_populates='meeting', cascade='all, delete-orphan')


class TranscriptSegment(Base):
    __tablename__ = 'transcript_segments'

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    speaker = Column(String(255), default='Speaker 1')
    start_time = Column(Float, default=0.0)
    end_time = Column(Float, default=0.0)
    text = Column(Text, nullable=False)

    meeting = relationship('Meeting', back_populates='segments')


class ActionItem(Base):
    __tablename__ = 'action_items'

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    description = Column(Text, nullable=False)
    assignee = Column(String(255), default='Unassigned')
    deadline = Column(String(255), default='Not specified')
    priority = Column(String(50), default='medium')
    status = Column(String(50), default='open')
    source_segment_id = Column(Integer, nullable=True)

    meeting = relationship('Meeting', back_populates='action_items')


class Decision(Base):
    __tablename__ = 'decisions'

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    decision = Column(Text, nullable=False)
    context = Column(Text, default='')
    source_segment_id = Column(Integer, nullable=True)
    timestamp = Column(Float, default=0.0)

    meeting = relationship('Meeting', back_populates='decisions')


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, default='')

    meeting = relationship('Meeting', back_populates='topics')


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, default='')
    source_segment_id = Column(Integer, nullable=True)

    meeting = relationship('Meeting', back_populates='questions')
