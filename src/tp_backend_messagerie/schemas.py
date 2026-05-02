""" 
Module qui gère ce que l'API accepte et renvoie.

"""

from sqlmodel import SQLModel, Field
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
    subject : str = Field(min_length = 1)
    body : str = Field(min_length = 1)

class MessageRead(SQLModel):
    id : int 
    sender_id : int 
    receiver_id : int 
    sent_at : datetime.datetime
    is_read : bool
    subject : str 
    body : str