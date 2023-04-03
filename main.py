from deta import Deta
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import *
import uvicorn
load_dotenv()


class MessageData(BaseModel):
    text: str


deta = Deta(os.getenv("DETA_PROJECT_KEY"))  # configure your Deta project
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Work in progress"}


@app.get("/users/{id}")
async def get_users_by_id(id: str):
    db = deta.Base("users")  # access your DB
    user = db.get(id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/thread/{id}")
async def get_thread_by_id(id: str):
    db = deta.Base("chatData")  # access your DB
    message = db.get(id)
    if message:
        return message
    raise HTTPException(status_code=404, detail="Thread not found")


@app.post("/thread")
async def send_message(sender_id: str, receiver_id: str, messageData: MessageData):
    db = deta.Base("chatData")
    thread = db.fetch({"participants.user_id": sender_id,
                      "participants.user_id2": receiver_id})
    if not thread.items:
        nThread = {
            "participants": 
                {"user_id": sender_id,
                 "user_id2": receiver_id},
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
