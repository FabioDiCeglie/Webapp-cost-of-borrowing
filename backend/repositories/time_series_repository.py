from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from domain.time_series import TimeSeriesObservation
from infrastructure.db.models import TimeSeriesObservationModel


class TimeSeriesRepository:
    def upsert_observations(self, db: Session, observations: list[TimeSeriesObservation]) -> int:
        if not observations:
            return 0

        rows = [{"period_date": o.period_date, "value": o.value} for o in observations]

        stmt = insert(TimeSeriesObservationModel).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TimeSeriesObservationModel.period_date],
            set_={"value": stmt.excluded.value},
        )
        db.execute(stmt)
        db.commit()
        return len(observations)

    def list_observations(
        self,
        db: Session,
        *,
        start: date | None = None,
        end: date | None = None,
    ) -> list[TimeSeriesObservation]:
        stmt = select(TimeSeriesObservationModel)
        if start is not None:
            stmt = stmt.where(TimeSeriesObservationModel.period_date >= start)
        if end is not None:
            stmt = stmt.where(TimeSeriesObservationModel.period_date <= end)

        stmt = stmt.order_by(TimeSeriesObservationModel.period_date.asc())
        models = db.execute(stmt).scalars().all()
        return [TimeSeriesObservation(period_date=m.period_date, value=m.value) for m in models]

