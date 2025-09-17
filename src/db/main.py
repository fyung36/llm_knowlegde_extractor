from sqlmodel import Session, SQLModel, create_engine

from src.config import settings

engine = create_engine(settings.POSTGRES_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
