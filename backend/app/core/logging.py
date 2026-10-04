import logging
from typing import Any

logger = logging.getLogger('meetingmind')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
    logger.addHandler(handler)


def log_event(event: str, **fields: Any) -> None:
    payload = {'event': event, **fields}
    logger.info(payload)
