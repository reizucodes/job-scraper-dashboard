from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.job_source import JobSource


class SQLAlchemyJobSourceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, source: JobSource) -> JobSource:
        self._session.add(source)
        self._session.flush()
        self._session.refresh(source)
        return source

    def get(self, source_id: int) -> JobSource | None:
        return self._session.get(JobSource, source_id)

    def list_all(self) -> list[JobSource]:
        stmt = select(JobSource).order_by(JobSource.id.asc())
        return list(self._session.scalars(stmt).all())

    def list_enabled(self) -> list[JobSource]:
        stmt = select(JobSource).where(JobSource.enabled.is_(True)).order_by(JobSource.id.asc())
        return list(self._session.scalars(stmt).all())

    def list_by_ids(self, source_ids: list[int]) -> list[JobSource]:
        if not source_ids:
            return []
        stmt = select(JobSource).where(JobSource.id.in_(source_ids)).order_by(JobSource.id.asc())
        return list(self._session.scalars(stmt).all())

    def update(self, source: JobSource) -> JobSource:
        self._session.add(source)
        self._session.flush()
        self._session.refresh(source)
        return source

    def delete(self, source_id: int) -> bool:
        entity = self.get(source_id)
        if entity is None:
            return False
        self._session.delete(entity)
        self._session.flush()
        return True
