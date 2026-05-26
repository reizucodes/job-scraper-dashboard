from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.job_bookmark import JobBookmark
from app.repositories.interfaces import JobBookmarkRepository, JobListingRepository
from app.schemas.bookmark import JobBookmarkUpsert
from app.services.errors import NotFoundError


class JobBookmarkService:
    def __init__(
        self,
        session: Session,
        bookmark_repository: JobBookmarkRepository,
        listing_repository: JobListingRepository,
    ) -> None:
        self._session = session
        self._bookmark_repository = bookmark_repository
        self._listing_repository = listing_repository

    def upsert(self, listing_id: int, payload: JobBookmarkUpsert) -> JobBookmark:
        listing = self._listing_repository.get(listing_id)
        if listing is None:
            raise NotFoundError(f"Job listing {listing_id} not found")

        bookmark = JobBookmark(
            job_id=listing.id,
            status=payload.status.value,
            notes=payload.notes,
            updated_at=datetime.now(timezone.utc),
        )
        result = self._bookmark_repository.upsert(bookmark)
        self._session.commit()
        self._session.refresh(result)
        return result
