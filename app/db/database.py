from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATA_BASE = config('DATABASE_URL')

engine = create_engine(DATA_BASE)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from app.models.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
