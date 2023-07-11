from sqlalchemy import Column, ForeignKey, String, Date, DateTime
from sqlalchemy.orm import relationship
from src.core.database.configs import settings
import datetime

class User(settings.DBBaseModel):
    __tablename__ = "users"
    id : str = Column(String(250), primary_key=True)
    nome_completo: str = Column(String(250), nullable=False)
    genero: str = Column(String(250), nullable=False)
    cpf: str = Column(String(250), nullable=False)
    email: str = Column(String(250), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    senha: str = Column(String(250), nullable=False)
    preferencia_comunicacao: str = Column(String(250), nullable=False)
    cep: str = Column(String(250), nullable=False)
    telefone: str = Column(String(250), nullable=False) 
    endereco: str = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Thread(settings.DBBaseModel):
    __tablename__ = "thread"
    id : str = Column(String(250), primary_key=True)
    participant_1: str = Column(String(250), ForeignKey("users.id"), nullable=False)
    participant_2: str = Column(String(250), ForeignKey("users.id"), nullable=False)
    participant1 = relationship("User", primaryjoin="Thread.participant_1==User.id")
    participant2 = relationship("User", primaryjoin="Thread.participant_2==User.id")

class Message(settings.DBBaseModel):
    __tablename__ = "message"
    id : str = Column(String(250), primary_key=True)
    thread_id: str = Column(String(250), ForeignKey("thread.id"), nullable=False)
    content: str = Column(String(128), nullable=False)
    sender_id: str = Column(String(250), ForeignKey("users.id"), nullable=False)
    receiver_id: str = Column(String(250), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    thread = relationship(Thread, backref='messages')
    sender = relationship('User', primaryjoin='Message.sender_id==User.id')
    receiver = relationship('User', primaryjoin='Message.receiver_id==User.id')


class Notification(settings.DBBaseModel):
    __tablename__ = "notification"
    id : str = Column(String(250), primary_key=True)
    message_id: str = Column(String(250), ForeignKey("message.id"), nullable=False)
    content: str = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    message = relationship(Message, backref='notification')