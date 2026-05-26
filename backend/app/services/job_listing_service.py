from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.db.models.job_listing import JobListing
from app.repositories.interfaces import JobBookmarkRepository, JobListingFilters, JobListingRepository


@dataclass(slots=True)
class PaginatedJobListings:
    items: list[JobListing]
    bookmark_status_by_listing_id: dict[int, str]
    limit: int
    offset: int


class JobListingService:
    def __init__(self, repository: JobListingRepository, bookmark_repository: JobBookmarkRepository) -> None:
        self._repository = repository
        self._bookmark_repository = bookmark_repository

    def list_listings(
        self,
        *,
        source_id: int | None,
        is_active: bool | None,
        work_mode: str | None,
        location: str | None,
        title_query: str | None,
        posted_from: datetime | None,
        posted_to: datetime | None,
        limit: int,
        offset: int,
    ) -> PaginatedJobListings:
        filters = JobListingFilters(
            source_id=source_id,
            is_active=is_active,
            work_mode=work_mode,
            location=location,
            title_query=title_query,
            posted_from=posted_from,
            posted_to=posted_to,
        )
        items = self._repository.list_filtered(filters=filters, limit=limit, offset=offset)
        bookmarks = self._bookmark_repository.list_by_job_ids([item.id for item in items])
        bookmark_status_by_listing_id = {bookmark.job_id: bookmark.status for bookmark in bookmarks}
        return PaginatedJobListings(
            items=items,
            bookmark_status_by_listing_id=bookmark_status_by_listing_id,
            limit=limit,
            offset=offset,
        )
