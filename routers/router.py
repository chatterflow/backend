from fastapi import FastAPI, HTTPException
from core.schemas.messageSchema import *
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


@app.post("/send_message")
async def send_message(sender_id: str, receiver_id: str, messageData: Message):
    if (receiver_id > sender_id):
        thread = db.fetch({"participants?contains": sender_id, "participants?contains": receiver_id})
    elif (sender_id == receiver_id):
        raise HTTPException(status_code=400, detail="Sender and receiver IDs cannot be the same")
    else: 
        thread = db.fetch({"participants?contains": receiver_id, "participants?contains": sender_id})
    if not thread.items:
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
    message_doc =  {
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

