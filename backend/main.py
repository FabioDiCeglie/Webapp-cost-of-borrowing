from fastapi import FastAPI, Response

from infrastructure.db.engine import get_db_engine, init_schema
from repositories.postgres_repository import PostgresRepository

app = FastAPI(title="Cost of borrowing API")

engine = get_db_engine()
postgres = PostgresRepository(engine)


@app.on_event("startup")
def startup() -> None:
    # Fail fast if DB is unreachable/misconfigured.
    postgres.ping()
    init_schema()


@app.get("/health", status_code=204)
def health() -> Response:
    return Response(status_code=204)

