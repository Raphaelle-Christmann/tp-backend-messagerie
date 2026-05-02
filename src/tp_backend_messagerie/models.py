"""Modèles SQLModel qui définissent les tables de données.

Ce module définit deux classes : 
- User
- Message
On aura une base de donnée (dans Messagerie.db) mais deux tables, une pour chaque classe.
"""

from sqlmodel import SQLModel, Field
import datetime

class User(SQLModel, table = True):
    """Représente un utilisateur de la messagerie.

    Attributs:
        id: identifiant de l'utilisateur.
        username: nom de l'utilisateur dans la messagerie.
        email: email de l'utilisateur.
    """
    id : int | None = Field(default = None, primary_key = True)
    username : str
    email : str

class Message(SQLModel, table = True):
    """Représente un message envoyé dans la messagerie.

    Attributs:
        id: identifiant du message.
        sender_id: identifiant de l'utilisateur qui envoie le message.
        receiver_id: identifiant de l'utilisateur qui reçoit le message.
        subject: sujet du message.
        body: corps du message.
        sent_at : heure et date d'envoi du message.
        is_read: statut du message (lu ou non).
    """
    id : int | None = Field(default = None, primary_key = True)
    sender_id : int | None = Field(foreign_key = "user.id")
    receiver_id : int | None = Field(foreign_key = "user.id")
    subject : str
    body : str
    sent_at : datetime.datetime = Field(default_factory = datetime.datetime.utcnow)
    is_read : bool | None = Field(default = False)