from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    nome_completo: str = None
    genero: str = None
    cpf: str = None
    email: str = None
    data_nascimento: date = None
    senha: str = None
    preferencia_comunicacao: str = None
    cep: str = None
    telefone: str = None
    endereco: str = None

    class Config:
        orm_mode: True

class Thread(BaseModel):
    participant_1: str = None
    participant_2: str = None

    class Config:
        orm_mode: True

class Message(BaseModel):
    content: str = None
    thread_id: str = None
    sender_id: str = None
    receiver_id: str = None
    creation_date: date = None

    class Config:
        orm_mode: True

class Notification(BaseModel):
    content: str = None
    message_id: str = None
    creation_date: date = None

    class Config:
        orm_mode: True
