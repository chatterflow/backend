from fastapi import Depends, HTTPException, APIRouter
from src.core.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.core.schemas.schemas import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.database import get_session
from src.core.repositories.messages_repository import MessageRepository
router = APIRouter()


@router.get("/messages")
async def get(db: AsyncSession = Depends(get_session)):
    try:
        msg = await MessageRepository(db).select_everything()
        return msg
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/message")
async def create(msg: Message, db: AsyncSession = Depends(get_session)):
    try:
        newMsg = await MessageRepository(db).create_message(msg)
        return newMsg
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/messsages/threadId/{threadId}")
async def get(threadId: str, db: AsyncSession = Depends(get_session)):
    try:
        threadInfo = await MessageRepository(db).get_all_msg_via_thread(threadId)
        return threadInfo
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
