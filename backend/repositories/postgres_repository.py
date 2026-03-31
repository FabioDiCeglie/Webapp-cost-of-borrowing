from sqlalchemy import text
from sqlalchemy.engine import Engine


class PostgresRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def ping(self) -> None:
        with self._engine.connect() as conn:
            conn.execute(text("SELECT 1"))

