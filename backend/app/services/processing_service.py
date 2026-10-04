from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.ai.extractor import extract_meeting_analysis, parse_action_items, parse_decisions
from app.ai.prompts.analysis import ANALYSIS_PROMPT
from app.core.config import PROCESSED_DIR
from app.core.logging import log_event
from app.utils.chunking import chunk_transcript


class ProcessingService:
    def __init__(self):
        self.process_root = PROCESSED_DIR

    def process_meeting(self, meeting_id: int, transcript: str, metadata: dict[str, Any]) -> dict[str, Any]:
        chunks = chunk_transcript(transcript, chunk_size=3, overlap=1, speaker='Speaker 1')
        analysis = extract_meeting_analysis(transcript)
        action_items = parse_action_items(transcript)
        decisions = parse_decisions(transcript)
        payload = {
            'meeting_id': meeting_id,
            'analysis': analysis,
            'chunks': chunks,
            'action_items': action_items,
            'decisions': decisions,
            'prompt': ANALYSIS_PROMPT,
            'meta': metadata,
        }
        output_path = self.process_root / f'meeting_{meeting_id}.json'
        output_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        log_event('meeting_processed', meeting_id=meeting_id, status='ok', chunks=len(chunks), action_items=len(action_items))
        return payload
