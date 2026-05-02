"""Module qui gère le routeur en charge des utilisateurs.

Il est séparé de celui des messages pour plus de clarté dans le code.
"""

from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session, select, desc
from tp_backend_messagerie.database import get_session
from tp_backend_messagerie.models import User, Message
from tp_backend_messagerie.schemas import UserCreate, UserRead, MessageRead

router = APIRouter()

@router.post("/users", response_model = UserRead, status_code = 201)
def create_users(user : UserCreate, session : Session = Depends(get_session)):
    """Crée un nouvel utilisateur.
    
    Paramètres:
        user: le ouvel utilisateur à ajouter sur la messagerie.
    
    Renvoie:
        UserRead: le nouvel utilisateur ajouté à la messagerie.
        
    Lève: 400 si le nom du nouvel utilisateur est déjà pris.
    """
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=user.username, email=user.email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/users", response_model = list[UserRead])
def get_all_users(session : Session = Depends(get_session)):
    """Récupère tous les utilisateurs.

    Renvoie:
        list[UserRead]: la liste de tous les utlisateurs de la messagerie.
    """
    return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model = UserRead)
def get_user_by_id(user_id : int, session : Session = Depends(get_session)):
    """Récupère un utilisateur par son identifiant.

    Paramètres: 
        user_id: identifiant de l'utilisateur recherché.

    Renvoie:
        UserRead: L'utilisateur correspondant.

    Lève:
        HTTPException: 404 si l'utilisateur n'existe pas.
    """
    user = session.get(User, user_id)
    if not user :
        raise HTTPException(status_code = 404, detail = "There is no user with this id.")
    return user

@router.get("/users/by_username/{username}", response_model = UserRead)
def get_user_by_username(username : str, session : Session = Depends(get_session)):
    """Récupère un utilisateur par son nom d'utilisateur.

    Paramètres: 
        username: nom d'utilisateur de l'utilisateur recherché.

    Renvoie:
        UserRead: L'utilisateur correspondant.

    Lève:
        HTTPException: 404 si l'utilisateur n'existe pas.
    """
    user = session.exec(select(User).where(User.username == username)).first()
    if not user :
        raise HTTPException(status_code = 404, detail = "There is no user with this username.")
    return user

@router.get("/users/{user_id}/inbox", response_model = list[MessageRead])
def get_inbox_by_id(user_id : int, unread_only : bool = False, session : Session = Depends(get_session)):
    """Récupère la boîte à message d'un utilisateur par son identifiant.

    Paramètres: 
        user_id: identifiant de l'utilisateur recherché.
        unread_only: affichage des messages non lus uniquement (True), ou bien tous (False).

    Renvoie:
        list[MessageRead]: la boîte à message de l'utilisateur correspondant.

    Lève:
        HTTPException: 404 si l'utilisateur n'existe pas.
    """
    user_exists = session.get(User, user_id)
    if not user_exists :
        raise HTTPException(status_code = 404, detail = "The user does not exists.")
    if unread_only :
        return session.exec(select(Message).where(Message.receiver_id == user_id).where(Message.is_read == False).order_by(desc(Message.sent_at))).all()
    all_messages_received = session.exec(select(Message).where(Message.receiver_id == user_id).order_by(desc(Message.sent_at))).all()
    return all_messages_received

@router.get("/users/{user_id}/sent", response_model = list[MessageRead])
def get_messages_sent_by_id(user_id : int, session : Session = Depends(get_session)):
    """Récupère les messages envoyés par un utilisateur par son identifiant.

    Paramètres: 
        user_id: identifiant de l'utilisateur recherché.

    Renvoie:
        list[MessageRead]: les messages envoyés par l'utilisateur correspondant.

    Lève:
        HTTPException: 404 si l'utilisateur n'existe pas.
    """
    user_exists = session.get(User, user_id)
    if not user_exists :
        raise HTTPException(status_code = 404, detail = "The user does not exists.")
    all_messages_sent = session.exec(select(Message).where(Message.sender_id == user_id).order_by(desc(Message.sent_at))).all()
    return all_messages_sent