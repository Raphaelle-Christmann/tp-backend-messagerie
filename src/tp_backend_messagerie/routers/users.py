"""
Module qui gère le routeur en charge des utilisateurs, on le sépare de celui des messages pour plus de clarté dans le code
"""

from fastapi import APIRouter, Depends, HTTPException 
from sqlmodel import Session, select
from tp_backend_messagerie.database import get_session
from tp_backend_messagerie.models import User 
from tp_backend_messagerie.schemas import UserCreate, UserRead

router = APIRouter()

@router.post("/users", response_model = UserRead, status_code = 201)
def create_users(user : UserCreate, session : Session = Depends(get_session)):
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
    return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model = UserRead)
def get_user_by_id(user_id : int, session : Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user :
        raise HTTPException(status_code = 404, detail = "There is no user with this id.")
    return user

@router.get("/users/by_username/{username}", response_model = UserRead)
def get_user_by_username(username : str, session : Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user :
        raise HTTPException(status_code = 404, detail = "There is no user with this username.")
    return user