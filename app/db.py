from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import get_settings

DATABASE_URL = get_settings().DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def get_session():
    with Session(engine) as session:
        yield session
