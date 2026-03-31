import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date

from fastapi import APIRouter, Depends, FastAPI, Response
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from adapters.ecb_portal_provider import EcbPortalProvider
from infrastructure.db.engine import get_db_engine, init_schema
from infrastructure.db.session import get_db
from repositories.postgres_repository import PostgresRepository
from repositories.time_series_repository import TimeSeriesObservationRepository
from services.cost_of_borrowing_households.schemas import IngestResponse, ObservationsResponse
from services.cost_of_borrowing_households.service import CostOfBorrowingHouseholdsService

engine = get_db_engine()
postgres = PostgresRepository(engine)
time_series_repo = TimeSeriesObservationRepository()
provider = EcbPortalProvider()
cost_of_borrowing_households_service = CostOfBorrowingHouseholdsService(provider, time_series_repo)

api = APIRouter(prefix="/api/v1")

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    postgres.ping()
    init_schema()

    # OK for this assignment/demo. In production, ingestion usually runs as a scheduled job/worker and the API stays stateless.
    try:
        with Session(engine) as db:
            ingested = cost_of_borrowing_households_service.ingest(db)
        logger.info("Ingested %s observations on startup", ingested)
    except Exception:
        logger.exception("Startup ingest failed; continuing without ingest")

    yield


app = FastAPI(title="Cost of borrowing API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@api.get("/health", status_code=204)
def health() -> Response:
    return Response(status_code=204)


@api.post("/ingest", response_model=IngestResponse)
def ingest(db: Session = Depends(get_db)) -> IngestResponse:
    ingested = cost_of_borrowing_households_service.ingest(db)
    return IngestResponse(ingested=ingested)


@api.get("/observations", response_model=list[ObservationsResponse])
def list_observations(
    start: date | None = None,
    end: date | None = None,
    db: Session = Depends(get_db),
) -> list[ObservationsResponse]:
    observations = cost_of_borrowing_households_service.get_observations(db, start=start, end=end)
    return [ObservationsResponse(period_date=o.period_date, value=o.value) for o in observations]


app.include_router(api)
