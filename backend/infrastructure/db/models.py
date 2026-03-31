from datetime import date

from sqlalchemy import Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.base import Base


class BorrowingCostObservationModel(Base):
    __tablename__ = "borrowing_cost_observations"

    period_date: Mapped[date] = mapped_column(Date, primary_key=True)
    value: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)

