from fastapi import FastAPI, Response
from sqlalchemy import text

from infrastructure.db.engine import get_db_engine, init_schema

app = FastAPI(title="Cost of borrowing API")

engine = get_db_engine()


@app.on_event("startup")
def startup() -> None:
    # Fail fast if DB is unreachable/misconfigured.
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    init_schema()


@app.get("/health", status_code=204)
def health() -> Response:
    return Response(status_code=204)

