from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    ingested: int = Field(ge=0)


class ObservationsResponse(BaseModel):
    period_date: date
    value: Decimal

