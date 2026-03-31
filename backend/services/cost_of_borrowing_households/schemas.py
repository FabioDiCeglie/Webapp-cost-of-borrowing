from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    ingested: int = Field(ge=0)


class ObservationOut(BaseModel):
    period_date: date
    value: Decimal

