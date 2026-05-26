from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.exporters import EXPORT_COLUMNS, ExportArtifact, ExporterRegistry
from app.repositories.interfaces import JobBookmarkRepository, JobListingFilters, JobListingRepository
from app.schemas.export import ExportFilters


@dataclass(slots=True)
class ExportResult:
    artifact: ExportArtifact
    filename: str


class ExportService:
    def __init__(
        self,
        listing_repository: JobListingRepository,
        bookmark_repository: JobBookmarkRepository,
        exporter_registry: ExporterRegistry,
    ) -> None:
        self._listing_repository = listing_repository
        self._bookmark_repository = bookmark_repository
        self._exporter_registry = exporter_registry

    def export(self, format_name: str, filters: ExportFilters) -> ExportResult:
        listing_filters = JobListingFilters(
            source_id=filters.source_id,
            is_active=filters.is_active,
            work_mode=filters.work_mode,
            location=filters.location,
            title_query=filters.title_query,
            posted_from=filters.posted_from,
            posted_to=filters.posted_to,
        )
        listings = self._listing_repository.list_filtered(
            filters=listing_filters,
            limit=filters.limit,
            offset=filters.offset,
        )

        bookmarks = self._bookmark_repository.list_by_job_ids([listing.id for listing in listings])
        bookmark_map = {bookmark.job_id: bookmark.status for bookmark in bookmarks}

        rows = [
            {
                "title": listing.title,
                "company": listing.company,
                "location": listing.location or "",
                "work_mode": listing.work_mode or "",
                "employment_type": listing.employment_type or "",
                "posted_at": listing.posted_at.isoformat() if listing.posted_at else "",
                "apply_url": listing.apply_url,
                "description_snippet": listing.description_snippet or "",
                "tags": ", ".join(listing.tags),
                "skills": ", ".join(listing.skills),
                "first_seen_at": listing.first_seen_at.isoformat(),
                "last_seen_at": listing.last_seen_at.isoformat(),
                "source_id": str(listing.source_id),
                "bookmark_status": bookmark_map.get(listing.id, "new"),
            }
            for listing in listings
        ]

        exporter = self._exporter_registry.resolve(format_name)
        artifact = exporter.export(rows=rows, columns=EXPORT_COLUMNS)

        generated_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"job-export-{generated_at}.{artifact.file_extension}"
        return ExportResult(artifact=artifact, filename=filename)
