from src.core.schemas import schemas
from src.core.models.models import Thread, Message
from src.core.utils.utils import value_exists, select_value, select_everything, select_value_all_order_by
from src.core.errors.errors import DuplicateEntryError, DatabaseError, NotFoundError
from datetime import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_message(self, messageSchema: schemas.Message):
        async with self.db as session:
            ThreadExists = await value_exists(self.db, Thread, Thread.id, messageSchema.thread_id)
            if not ThreadExists:
                raise DuplicateEntryError("Thread doesn't exist")

            newMessage = Message(
                id=str(uuid.uuid4()),
                thread_id=messageSchema.thread_id,
                content=messageSchema.content,
                sender_id=messageSchema.sender_id,
                receiver_id=messageSchema.receiver_id,
                created_at=datetime.now(),
            )
            try:
                session.add(newMessage)
                await session.commit()
                return newMessage
            except Exception as error:
                await session.rollback()
                print(f"Error when inserting data into the database: {str(error)}")
                raise DatabaseError(
                    f"Error when inserting user data into the database: {str(error)}")

    async def get(self, messageId: str):
        message = await select_value(self.db, Message, Message.id, messageId)
        if not message:
            raise NotFoundError('Message not found')

        return message
    
    async def get_all_msg_via_thread(self, thread_id: str):
        message = await select_value_all_order_by(self.db, Message, Message.thread_id, thread_id, Message.created_at)
        if not message:
            raise NotFoundError('Message not found')

        return message

    async def get_by_user(self, sender_id: str):
        user = await select_value(self.db, Message, Message.sender_id, sender_id)
        if not user:
            raise NotFoundError('User not found')

        return user

    async def select_everything(self):
        msg = await select_everything(self.db, Message)
        if not msg:
            raise NotFoundError('Something went wrong')
        return msg
