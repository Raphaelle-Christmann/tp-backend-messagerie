""" Module qui gère ce que l'API accepte et renvoie (schémas de validation).
"""

from sqlmodel import SQLModel, Field
import datetime
from pydantic import EmailStr

class UserCreate(SQLModel):
    """Schéma de validation pour la création d'un utilisateur.

    Attributs:
        username: nom de l'utilisateur créé.
        email: email de l'utilisateur créé.
    """
    username : str
    email : EmailStr

class UserRead(SQLModel):
    """Schéma de réponse pour la lecture d'un utilisateur.

    Attributs:
        id: identifiant de l'utilisateur.
        username: nom de l'utilisateur.
        email: email de l'utilisateur.
    """
    id : int
    username : str 
    email : str

class MessageCreate(SQLModel):
    """Schéma de validation pour la création d'un message.

    Attributs:
        sender_id: identifiant de l'expéditeur.
        receiver_id: identifiant du receveur.
        subject: sujet du message créé.
        body: corps du message créé.
    """
    sender_id : int
    receiver_id : int
    subject : str = Field(min_length = 1)
    body : str = Field(min_length = 1)

class MessageRead(SQLModel):
    """Schéma de réponse pour la lecture d'un message.

    Attributs:
        id: identifiant du message.
        sender_id: identifiant de l'expéditeur.
        receiver_id: identifiant du receveur.
        sent_at: heure et date d'envoi du message.
        is_read: statut du message (lu ou non).
        subject: sujet du message créé.
        body: corps du message créé.
    """
    id : int 
    sender_id : int 
    receiver_id : int 
    sent_at : datetime.datetime
    is_read : bool
    subject : str 
    body : str