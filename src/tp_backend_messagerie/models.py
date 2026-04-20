"""Fichier qui définit ce qu'on stocke dans la base de données, ceci est fait via deux classes :
- User : représente un utilisateur de l'application
- Message : représente un message échnagé sur la messagerie

On aura une base de donnée (dans Messagerie.db) mais deux tables, une pour chaque classe.
"""

from sqlmodel import SQLModel, Field
import datetime

class User(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    username : str
    email : str

class Message(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    sender_id : int | None = Field(foreign_key = "user.id")
    receiver_id : int | None = Field(foreign_key = "user.id")
    subject : str
    body : str
    sent_at : datetime.datetime = Field(default_factory = datetime.datetime.utcnow)
    is_read : bool | None = Field(default = False)