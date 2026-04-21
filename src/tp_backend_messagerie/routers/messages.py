"""
Module qui gère le routeur en charge des messages, on le sépare de celui des utilisateurs pour plus de clarté dans le code
"""

from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session
from tp_backend_messagerie.database import get_session
from tp_backend_messagerie.models import Message, User
from tp_backend_messagerie.schemas import MessageCreate, MessageRead

router = APIRouter()

@router.post("/messages", response_model = MessageRead, status_code = 201)
def send_messages(to_send : MessageCreate, session : Session = Depends(get_session)):
    sender_exists = session.get(User, to_send.sender_id)
    if not sender_exists :
        raise HTTPException(status_code = 404, detail = "The sender does not exists.")
    receiver_exists = session.get(User, to_send.receiver_id)
    if not receiver_exists :
        raise HTTPException(status_code = 404, detail = "The receiver does not exists.")
    if to_send.sender_id == to_send.receiver_id :
        raise HTTPException(status_code = 400, detail = "The sender and the receiver are the same.")
    message = Message(sender_id = to_send.sender_id, receiver_id = to_send.receiver_id, subject = to_send.subject, body = to_send.body)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

@router.get("/messages/{message_id}", response_model = MessageRead)
def get_message_by_id(message_id : int, session : Session = Depends(get_session)):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="The message does not exists.")
    return message

@router.patch("/messages/{message_id}/read", response_model = MessageRead)
def message_is_read(message_id : int, session : Session = Depends(get_session)):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="The message does not exists.")
    message.is_read = True
    session.commit()
    session.refresh(message)
    return message