from fastapi import APIRouter

router = APIRouter()


@router.get('/search')
def search():
    return {'results': []}
