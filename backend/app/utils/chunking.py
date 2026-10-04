from __future__ import annotations

from typing import Any


def chunk_transcript(text: str, chunk_size: int = 4, overlap: int = 1, speaker: str = 'Speaker 1') -> list[dict[str, Any]]:
    if not text:
        return []
    sentences = [part.strip() for part in text.split('.') if part.strip()]
    chunks: list[dict[str, Any]] = []
    for index in range(0, len(sentences), max(1, chunk_size - overlap)):
        current = sentences[index:index + chunk_size]
        if not current:
            continue
        chunk_text = '. '.join(current) + '.'
        chunks.append({
            'speaker': speaker,
            'start_time': float(index),
            'end_time': float(index + len(current)),
            'text': chunk_text,
        })
    return chunks
