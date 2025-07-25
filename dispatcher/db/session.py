from typing import Generator

from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_engine() -> Generator[SessionLocal, None, None]:  # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
