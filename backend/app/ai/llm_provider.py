from __future__ import annotations

import os
from typing import Any


class DemoLLM:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or ''
        self.base_url = base_url or ''
        self.model = model or 'demo-model'

    def generate(self, prompt: str, context: str = '') -> str:
        if not context:
            return 'Demo mode: the application generated a grounded response using the available transcript text.'
        return f"Demo answer based on the meeting context: {context[:450]}"


def get_llm_provider() -> DemoLLM:
    return DemoLLM()
