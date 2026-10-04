from fastapi import APIRouter

router = APIRouter()


@router.get('/analysis')
def analysis():
    return {'status': 'demo'}
