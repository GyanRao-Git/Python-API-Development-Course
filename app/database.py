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


# to do raw sql, use psychopg, in main.py on top ---------------------------------------------------------------------------------

# try:
#     conn = psycopg2.connect(
#         host=settings.DB_HOST, database=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("DB connection was succesfull..")
# except Exception as error:
#     print("Connection to db failed...")
#     print("Error: ", error)
#     time.sleep(2)
