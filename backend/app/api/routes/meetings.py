from fastapi import APIRouter

router = APIRouter()


@router.get('/meetings')
def list_meetings():
    return {'meetings': []}
