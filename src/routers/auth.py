from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from src.core.database.database import token_verifier

router = APIRouter(dependencies=[Depends(token_verifier)])

@router.get('/authorize')
def authenticate_user():
    return JSONResponse (
        content=True,
        status_code=status.HTTP_200_OK
    )