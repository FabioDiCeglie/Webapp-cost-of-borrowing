import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from infrastructure.db.base import Base
from infrastructure.db import models  # noqa: F401


@lru_cache
def get_db_engine() -> Engine:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required but was not set")
    return create_engine(database_url, pool_pre_ping=True)


def init_schema() -> None:
    env = os.environ.get("ENV", "dev").lower()
    if env != "dev":
        return

    engine = get_db_engine()
    Base.metadata.create_all(bind=engine)

