from fastapi import FastAPI, HTTPException
from core.schemas.messageSchema import Message
from core.database.database import db
from datetime import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Work in progress"}


@app.get("/thread/{id}")
async def get_thread_by_id(id: str):
    message = db.get(id)
    if message:
        return message
    raise HTTPException(status_code=404, detail="Thread not found")


@app.post("/send_first_message")
async def send_first_message(sender_id: str, receiver_id: str, messageData: Message):
    nThread = {
        "participants": [sender_id, receiver_id],
        "messages": [
            {
                "content": messageData.text,
                "created_at": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                "sender_id": sender_id,
                "receiver_id": receiver_id
            },
        ]
    }
    db.insert(nThread)
    return {'message': 'Message sent sucessfully'}


@app.post("/send_message")
async def send_message(thread_id: str, sender_id: str, messageData: Message):
    thread = db.fetch({"key": thread_id})
    if not thread.items:
        raise HTTPException(status_code=404, detail="Thread not found")
    for x in thread.items:
        for message in x['messages']:
            if sender_id != message['receiver_id']:
                receiver_id = message['receiver_id']
                break
    message_doc = {
        "content": messageData.text,
        "created_at": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
        "sender_id": sender_id,
        "receiver_id": receiver_id
    }
    append_message = {'messages': db.util.append(message_doc)}
    for i in thread.items:
        key = i['key']
    db.update(append_message, key=key)
    return {'message': 'Message sent successfully'}
