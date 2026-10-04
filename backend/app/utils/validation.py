from pathlib import Path

ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.mp4', '.webm'}


def validate_upload_filename(filename: str) -> str:
    name = Path(filename).name
    if not name or name in {'.', '..'}:
        raise ValueError('Invalid filename.')
    suffix = Path(name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError('Unsupported file type. Use MP3, WAV, M4A, MP4, or WEBM.')
    return name
