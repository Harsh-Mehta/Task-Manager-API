from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import PROD_DATABASE_URL

engine = create_engine(
    PROD_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()