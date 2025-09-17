from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from uuid import uuid4
from src.config import settings

Base = declarative_base()

JSONType = JSONB if not settings.USE_SQLITE else JSON

class Analysis(Base):
    __tablename__ = "analyses"

    uid = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid4
    )

    text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)

    title = Column(String, nullable=True)
    topics = Column(JSONType, nullable=False, default=list)
    sentiment = Column(String, nullable=False, default="neutral")
    keywords = Column(JSONType, nullable=False, default=list)
