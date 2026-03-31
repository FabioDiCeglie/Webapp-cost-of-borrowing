from fastapi import Depends, FastAPI, Response
from sqlalchemy.orm import Session

from adapters.ecb_portal_provider import EcbPortalProvider
from infrastructure.db.engine import get_db_engine, init_schema
from infrastructure.db.session import get_db
from repositories.postgres_repository import PostgresRepository
from repositories.time_series_repository import TimeSeriesRepository
from services.cost_of_borrowing_households.schemas import IngestResponse
from services.cost_of_borrowing_households.service import IngestCostOfBorrowingHouseholdsService

app = FastAPI(title="Cost of borrowing API")

engine = get_db_engine()
postgres = PostgresRepository(engine)
time_series_repo = TimeSeriesRepository()
provider = EcbPortalProvider()
ingest_service = IngestCostOfBorrowingHouseholdsService(provider, time_series_repo)


@app.on_event("startup")
def startup() -> None:
    # Fail fast if DB is unreachable/misconfigured.
    postgres.ping()
    init_schema()


@app.get("/health", status_code=204)
def health() -> Response:
    return Response(status_code=204)


@app.post("/ingest", response_model=IngestResponse)
def ingest(db: Session = Depends(get_db)) -> IngestResponse:
    ingested = ingest_service.ingest(db)
    return IngestResponse(ingested=ingested)

