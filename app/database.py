from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_CONNECTION_STRING= f'postgresql://postgres:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_CONNECTION_STRING)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base=declarative_base()