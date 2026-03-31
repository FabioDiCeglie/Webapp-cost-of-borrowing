import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@lru_cache
def get_db_engine() -> Engine:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required but was not set")
    return create_engine(database_url, pool_pre_ping=True)

