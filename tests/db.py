from sqlalchemy import create_engine
from src.config import settings

engine = create_engine(settings.DATABASE_URL)
conn = engine.connect()
print("Connected!")
conn.close()
