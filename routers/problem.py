from fastapi import HTTPException, APIRouter
from core.schemas.messageSchema import Message
from core.database.database import db
from datetime import *

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Work in progress"}


