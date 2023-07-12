from fastapi import FastAPI, WebSocket
from typing import List, Dict

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, thread_id: str):
        if thread_id not in self.active_connections:
            self.active_connections[thread_id] = []
        self.active_connections[thread_id].append(websocket)
        await websocket.accept()

    def disconnect(self, websocket: WebSocket, thread_id: str):
        if thread_id in self.active_connections:
            self.active_connections[thread_id].remove(websocket)

    async def broadcast(self, message: str, thread_id: str):
        if thread_id in self.active_connections:
            for connection in self.active_connections[thread_id]:
                await connection.send_text(message)
