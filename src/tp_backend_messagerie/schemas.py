""" 
Module de gestion de ce que l'API accepte et renvoie.

"""

from sqlmodel import SQLModel
import datetime

class UserCreate(SQLModel):
    username : str
    email : str

class UserRead(SQLModel):
    id : int
    username : str 
    email : str

class MessageCreate(SQLModel):
    sender_id : int
    receiver_id : int
    subject : str 
    body : str 

class MessageRead(SQLModel):
    id : int 
    sender_id : int 
    receiver_id : int 
    sent_at : datetime.datetime
    is_read : bool
    subject : str 
    body : str 