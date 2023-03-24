from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

import os

import MySQLdb

connection = MySQLdb.connect(

  host= os.getenv("HOST"),

  user=os.getenv("USERNAME"),

  passwd= os.getenv("PASSWORD"),

  db= os.getenv("DATABASE"),

  ssl_mode = "VERIFY_IDENTITY",

  ssl      = {

    "ca": "/etc/ssl/cert.pem"

  }

)



app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str

students = [
    {
        "id": 0,
        "name": "Pedro",
        "age": 20,
        "email": "pedro.laraburu@example.com"
    }
]


@app.get("/")
async def root():
    return {"message": "Hello World"}