from fastapi import Depends, HTTPException, APIRouter
from src.core.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.core.schemas.schemas import Thread
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.database import get_session
from src.core.repositories.thread_repository import ThreadRepository
router = APIRouter()


@router.get("/threads")
async def get(db: AsyncSession = Depends(get_session)):
    try:
        thread = await ThreadRepository(db).select_everything()
        return thread
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.get("/thread/id/{threadId}")
async def get(threadId:str, db: AsyncSession = Depends(get_session)):
    try:
        threadInfo = await ThreadRepository(db).get(threadId)
        return threadInfo
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    
@router.get("/thread/participants/{participant_1}/{participant_2}")
async def get(participant_1:str, participant_2: str, db: AsyncSession = Depends(get_session)):
    try:
        threadInfo = await ThreadRepository(db).get_thread_by_participants(pp_1=participant_1, pp_2=participant_2)
        return threadInfo
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.get("/thread/participant/{participant_1}")
async def get(participant_1:str, db: AsyncSession = Depends(get_session)):
    try:
        threadInfo = await ThreadRepository(db).get_thread_by_oneParticipant(pp_1=participant_1)
        return threadInfo
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/thread")
async def create(thread: Thread, db: AsyncSession = Depends(get_session)):
    try:
        thread = await ThreadRepository(db).create_thread(thread)
        return thread
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.delete("/thread")
async def delete(threadId: str, db: AsyncSession = Depends(get_session)):
    try:
        thread = await ThreadRepository(db).delete_thread(threadId)
        return thread
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))