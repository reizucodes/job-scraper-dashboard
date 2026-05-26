from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.job_bookmark import JobBookmark


class SQLAlchemyJobBookmarkRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert(self, bookmark: JobBookmark) -> JobBookmark:
        existing = self.get_by_job_id(bookmark.job_id)
        if existing is None:
            self._session.add(bookmark)
            self._session.flush()
            self._session.refresh(bookmark)
            return bookmark

        existing.status = bookmark.status
        existing.notes = bookmark.notes
        existing.updated_at = bookmark.updated_at
        self._session.add(existing)
        self._session.flush()
        self._session.refresh(existing)
        return existing

    def get_by_job_id(self, job_id: int) -> JobBookmark | None:
        stmt = select(JobBookmark).where(JobBookmark.job_id == job_id)
        return self._session.scalars(stmt).one_or_none()

    def list_by_job_ids(self, job_ids: list[int]) -> list[JobBookmark]:
        if not job_ids:
            return []
        stmt = select(JobBookmark).where(JobBookmark.job_id.in_(job_ids))
        return list(self._session.scalars(stmt).all())
