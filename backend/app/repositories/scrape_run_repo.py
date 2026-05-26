from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.scrape_run import ScrapeRun


class SQLAlchemyScrapeRunRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, run: ScrapeRun) -> ScrapeRun:
        self._session.add(run)
        self._session.flush()
        self._session.refresh(run)
        return run

    def get(self, run_id: int) -> ScrapeRun | None:
        return self._session.get(ScrapeRun, run_id)

    def list_recent(self, limit: int = 50) -> list[ScrapeRun]:
        stmt = select(ScrapeRun).order_by(ScrapeRun.started_at.desc()).limit(limit)
        return list(self._session.scalars(stmt).all())

    def update(self, run: ScrapeRun) -> ScrapeRun:
        self._session.add(run)
        self._session.flush()
        self._session.refresh(run)
        return run
