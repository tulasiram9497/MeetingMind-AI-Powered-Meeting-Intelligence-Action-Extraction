from fastapi import APIRouter

router = APIRouter()


@router.post('/transcribe')
def transcribe():
    return {'status': 'demo'}
