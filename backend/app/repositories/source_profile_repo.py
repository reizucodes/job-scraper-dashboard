from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.source_profile import SourceProfile


class SQLAlchemySourceProfileRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_all(self) -> list[SourceProfile]:
        stmt = select(SourceProfile).order_by(SourceProfile.code.asc())
        return list(self._session.scalars(stmt).all())

    def list_active(self) -> list[SourceProfile]:
        stmt = select(SourceProfile).where(SourceProfile.active.is_(True)).order_by(SourceProfile.code.asc())
        return list(self._session.scalars(stmt).all())

    def get(self, profile_id: int) -> SourceProfile | None:
        return self._session.get(SourceProfile, profile_id)

    def get_by_code(self, code: str) -> SourceProfile | None:
        stmt = select(SourceProfile).where(SourceProfile.code == code)
        return self._session.scalars(stmt).one_or_none()
