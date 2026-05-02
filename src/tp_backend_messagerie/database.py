"""Module de gestion de la base de données de la messagerie."""

from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./messagerie.db"

engine = create_engine(DATABASE_URL, echo = True)

def init_db():
    """Initialise la base de données de notre messagerie, en créant les tables SQL si elles n'existent pas.
    Elle doit être appelée au démarrage de la messagerie.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """Donne une session de base de données pour les routes FastAPI.
    C'est une dépendance FastAPI (ouverture de session, qui est transmise à la route, fermeture de la session après exécution.)
    
    Yields:
        Session: une session SQLModel active et prêt à être utilisée.
    """
    with Session(engine) as session:
        yield session