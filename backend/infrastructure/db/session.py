from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from infrastructure.db.engine import get_db_engine

engine = get_db_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

