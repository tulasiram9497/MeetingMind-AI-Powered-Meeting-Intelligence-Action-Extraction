from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_chunking_preserves_metadata():
    from app.utils.chunking import chunk_transcript

    text = ' '.join([f'Sentence {i}.' for i in range(1, 12)])
    chunks = chunk_transcript(text, chunk_size=3, overlap=1)
    assert len(chunks) > 0
    assert 'text' in chunks[0]
    assert 'start_time' in chunks[0]


def test_analysis_schema_validation():
    from app.ai.extractor import validate_analysis

    data = {
        'executive_summary': 'Summary',
        'detailed_summary': 'Detailed',
        'key_points': ['point'],
        'decisions': [],
        'action_items': [],
        'deadlines': [],
        'questions': [],
        'risks': [],
        'topics': [],
        'sentiment': {'overall': 'neutral', 'confidence': 0.8},
    }
    assert validate_analysis(data) is not None
