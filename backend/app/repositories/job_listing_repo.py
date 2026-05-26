from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models.job_listing import JobListing
from app.repositories.interfaces import JobListingFilters


class SQLAlchemyJobListingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, listing: JobListing) -> JobListing:
        self._session.add(listing)
        self._session.flush()
        self._session.refresh(listing)
        return listing

    def get(self, listing_id: int) -> JobListing | None:
        return self._session.get(JobListing, listing_id)

    def get_by_canonical_key(self, canonical_key: str) -> JobListing | None:
        stmt = select(JobListing).where(JobListing.canonical_key == canonical_key)
        return self._session.scalars(stmt).one_or_none()

    def list_filtered(self, filters: JobListingFilters, limit: int = 100, offset: int = 0) -> list[JobListing]:
        stmt: Select[tuple[JobListing]] = select(JobListing)

        if filters.source_id is not None:
            stmt = stmt.where(JobListing.source_id == filters.source_id)
        if filters.is_active is not None:
            stmt = stmt.where(JobListing.is_active.is_(filters.is_active))
        if filters.work_mode is not None:
            stmt = stmt.where(JobListing.work_mode.ilike(f"%{filters.work_mode}%"))
        if filters.location is not None:
            stmt = stmt.where(JobListing.location.ilike(f"%{filters.location}%"))
        if filters.title_query is not None:
            stmt = stmt.where(JobListing.title.ilike(f"%{filters.title_query}%"))
        if filters.posted_from is not None:
            stmt = stmt.where(JobListing.posted_at >= filters.posted_from)
        if filters.posted_to is not None:
            stmt = stmt.where(JobListing.posted_at <= filters.posted_to)

        stmt = stmt.order_by(JobListing.posted_at.desc().nullslast(), JobListing.id.desc()).limit(limit).offset(offset)
        return list(self._session.scalars(stmt).all())

    def update(self, listing: JobListing) -> JobListing:
        self._session.add(listing)
        self._session.flush()
        self._session.refresh(listing)
        return listing
