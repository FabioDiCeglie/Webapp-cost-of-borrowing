from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class TimeSeriesObservationModel(Base):
    __tablename__ = "time_series_observations"

    period_date: Mapped[date] = mapped_column(Date, primary_key=True)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)

