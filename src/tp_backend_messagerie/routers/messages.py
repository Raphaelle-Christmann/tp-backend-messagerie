"""Module qui gère le routeur en charge des messages.

Il est séparé de celui des utilisateurs pour plus de clarté dans le code.
"""

from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session
from tp_backend_messagerie.database import get_session
from tp_backend_messagerie.models import Message, User
from tp_backend_messagerie.schemas import MessageCreate, MessageRead

router = APIRouter()

@router.post("/messages", response_model = MessageRead, status_code = 201)
def send_messages(to_send : MessageCreate, session : Session = Depends(get_session)):
    """Envoie un message d'un utilisateur à un autre (différent de lui).
    
    Paramètres:
        to_send: message à envoyer.
    
    Renvoie:
        MessageRead: message envoyé.
        
    Lève:
        HTTPException: 404 si l'envoyeur n'existe pas.
        HTTPException: 404 si le receveur n'existe pas.
        HTTPException: 400 si le receveur et l'envoyeur sont la même personne.
    """
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
    """Récupère un message par son identifiant.

    Paramètres: 
        message_id: identifiant du message recherché.

    Renvoie:
        MessageRead: Le message correspondant.

    Lève:
        HTTPException: 404 si le message n'existe pas.
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="The message does not exists.")
    return message

@router.patch("/messages/{message_id}/read", response_model = MessageRead)
def message_is_read(message_id : int, session : Session = Depends(get_session)):
    """Met un message comme étant vu.
    
    Paramètres:
        message_id: identifiant du message à afficher comme étant lu.
        
    Renvoie:
        MessageRead: le message lu.
    
    Lève:
        HTTPException: 404 si le message n'existe pas.
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="The message does not exists.")
    message.is_read = True
    session.commit()
    session.refresh(message)
    return message

@router.delete("/messages/{message_id}")
def delete_message(message_id : int, session : Session = Depends(get_session)):
    """Supprime un message.
    
    Paramètres:
        message_id: identifiant du message à supprimer.
    
    Renvoie:
        dict: confirmation de la suppression.
    
    Lève:
        HTTPException: 404 si le message n'existe pas.
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="The message you want to delete does not exists.")
    session.delete(message)
    session.commit()
    return {"message": "Message deleted successfully"}