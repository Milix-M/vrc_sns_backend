from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.settings import settings
from api.db.models.user_model import User

def create_database() -> None:
    """Create a database."""
    engine:str = create_engine(settings.db_url)

    User.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()