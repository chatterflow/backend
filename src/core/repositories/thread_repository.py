from src.core.schemas import schemas
from src.core.models.models import Thread, User
from src.core.dto.dto import CreateThreadOutput
from src.core.utils.utils import select_value, select_everything, delete_value, select_value_and_or, value_exists_and_or, select_value_or
from src.core.errors.errors import DuplicateEntryError, DatabaseError, NotFoundError
import uuid

from sqlalchemy.ext.asyncio import AsyncSession


class ThreadRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_thread(self, threadSchema: schemas.Thread):
        async with self.db as session:
            ThreadExists = await value_exists_and_or(self.db, Thread, Thread.participant_1, threadSchema.participant_1, Thread.participant_2, threadSchema.participant_2)
            if ThreadExists:
                raise DuplicateEntryError("Thread already exists")

            newThread = Thread(
                id=str(uuid.uuid4()),
                participant_1 = threadSchema.participant_1,
                participant_2 = threadSchema.participant_2
            )
            threadOutput = CreateThreadOutput(
                id = newThread.id,
                participant_1= newThread.participant_1,
                participant_2= newThread.participant_2
            )
            try:
                session.add(newThread)
                await session.commit()
                return threadOutput
            except Exception as error:
                await session.rollback()
                print(f"Error when inserting data into the database: {str(error)}")
                raise DatabaseError(
                    f"Error when inserting user data into the database: {str(error)}")

    async def get(self, threadId: str):
        thread = await select_value(self.db, Thread, Thread.id, threadId)
        if not thread:
            raise NotFoundError('Thread not found')

        return thread
    
    async def get_thread_by_oneParticipant(self, pp_1: str):
        thread = await select_value_or(self.db, Thread, User, Thread.participant_1, pp_1, Thread.participant_2)
        if not thread:
            raise NotFoundError('Thread not found')

        return thread
    
    async def get_thread_by_participants(self, pp_1: str, pp_2: str):
        thread = await select_value_and_or(self.db, Thread, Thread.participant_1, pp_1, Thread.participant_2, pp_2)
        if not thread:
            raise NotFoundError('Thread not found')

        return thread
    
    async def delete_thread(self, threadId: str):
        thread = await delete_value(self.db, Thread, Thread.id, threadId)
        if not thread:
            raise NotFoundError('Thread not found')

        return thread

    async def select_everything(self):
        thread = await select_everything(self.db, Thread)
        if not thread:
            raise NotFoundError('Something went wrong')
        return thread
