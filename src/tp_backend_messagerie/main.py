"""Module de gestion globale de la messagerie.

Il gère :
- la création de l'application FastAPI
- l'initialisation des tables au démarrage via l'appel à init_db()
- le branchement des routers
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from tp_backend_messagerie.database import init_db
from tp_backend_messagerie.models import User, Message
from tp_backend_messagerie.routers import users
from tp_backend_messagerie.routers import messages

@asynccontextmanager
async def lifespan(app : FastAPI):
    """Initialise la base de donnée de la messagerie.
    
    Paramètres:
        app: l'application FastAPI de messagerie.
    
    Renvoie:
        Generator: cède le contrôle à l'application après le lancement, et gère l'arrêt lorsque on termine l'appli."""
    init_db() 
    yield

app = FastAPI(lifespan = lifespan)
app.include_router(users.router)
app.include_router(messages.router)