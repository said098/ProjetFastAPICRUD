from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", "5432")
DB_NAME = getenv("DB_NAME", "bnpdb")
DB_USER = getenv("DB_USER", "bnp")
DB_PASSWORD = getenv("DB_PASSWORD", "bnp123")

DATABASE_URL = (f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"f"@{DB_HOST}:{DB_PORT}/{DB_NAME}")

Base = declarative_base()


class DatabaseConnection:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL,pool_pre_ping=True,)
        self._SessionLocal = sessionmaker(bind=self.engine, autoflush=False)

    def get_session(self):
        db = self._SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            yield db
        finally:
            db.close()


# instance à utiliser partout
db_conn = DatabaseConnection()
engine = db_conn.engine


# Dépendance FastAPI pratique:
def get_db():
    yield from db_conn.get_session()
