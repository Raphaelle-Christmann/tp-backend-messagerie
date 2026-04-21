"""
Module qui gère :
- la création de l'application FastAPI
- l'initialisation des tables au démarrage via l'appel à init_db()
- branchement des routers
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from tp_backend_messagerie.database import init_db
from tp_backend_messagerie.models import User, Message
from tp_backend_messagerie.routers import users
from tp_backend_messagerie.routers import messages

@asynccontextmanager
async def lifespan(app : FastAPI):
    init_db() 
    yield

app = FastAPI(lifespan = lifespan)
app.include_router(users.router)
app.include_router(messages.router)