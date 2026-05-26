from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.raw_job import RawJob


class SQLAlchemyRawJobRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, raw_job: RawJob) -> RawJob:
        self._session.add(raw_job)
        self._session.flush()
        self._session.refresh(raw_job)
        return raw_job

    def list_by_run(self, scrape_run_id: int) -> list[RawJob]:
        stmt = select(RawJob).where(RawJob.scrape_run_id == scrape_run_id).order_by(RawJob.id.asc())
        return list(self._session.scalars(stmt).all())
