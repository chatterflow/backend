from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
import json
from fastapi.encoders import jsonable_encoder
from src.core.schemas.schemas import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.database import get_session
from src.core.repositories.messages_repository import MessageRepository
from src.core.repositories.websocket_repository import ConnectionManager
router = APIRouter()

manager = ConnectionManager()


@router.websocket("/ws/{thread_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, thread_id: str, db: AsyncSession = Depends(get_session)):
    await manager.connect(websocket, thread_id)
    try:
        while True:
            data = await websocket.receive_json()
            msg_data = Message(**data)
            newMsg = await MessageRepository(db).createMessage(msg_data)
            json_compatible_item_data = jsonable_encoder(newMsg)
            await manager.broadcast(json.dumps(json_compatible_item_data), thread_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, thread_id)
