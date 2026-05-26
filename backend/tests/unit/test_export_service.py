from __future__ import annotations

from datetime import datetime, timezone

from app.db.models.job_bookmark import JobBookmark
from app.db.models.job_listing import JobListing
from app.db.models.job_source import JobSource
from app.db.models.source_profile import SourceProfile
from app.exporters import CsvExporter, ExporterRegistry, XlsxExporter
from app.repositories.job_bookmark_repo import SQLAlchemyJobBookmarkRepository
from app.repositories.job_listing_repo import SQLAlchemyJobListingRepository
from app.schemas.export import ExportFilters
from app.services.export_service import ExportService


def _seed_source(db_session) -> JobSource:
    profile = SourceProfile(code="greenhouse", display_name="Greenhouse", active=True)
    db_session.add(profile)
    db_session.commit()
    source = JobSource(name="GH", base_url="https://jobs.example.com", profile_id=profile.id, enabled=True, config={})
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)
    return source


def test_export_service_filter_parity_and_bookmark_status(db_session) -> None:
    source = _seed_source(db_session)

    listing_1 = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="k1",
        title="Python Engineer",
        company="Acme",
        location="Remote",
        work_mode="remote",
        employment_type="full-time",
        posted_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        apply_url="https://jobs.example.com/1",
        description_snippet="Build APIs",
        tags=["backend"],
        skills=["Python"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    listing_2 = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="k2",
        title="Frontend Engineer",
        company="Acme",
        location="Manila",
        work_mode="hybrid",
        employment_type="full-time",
        posted_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        apply_url="https://jobs.example.com/2",
        description_snippet="Build UI",
        tags=["frontend"],
        skills=["Vue"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    db_session.add_all([listing_1, listing_2])
    db_session.commit()
    db_session.refresh(listing_1)

    bookmark = JobBookmark(
        job_id=listing_1.id,
        status="applied",
        notes=None,
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(bookmark)
    db_session.commit()

    service = ExportService(
        listing_repository=SQLAlchemyJobListingRepository(db_session),
        bookmark_repository=SQLAlchemyJobBookmarkRepository(db_session),
        exporter_registry=ExporterRegistry(exporters=[CsvExporter(), XlsxExporter()]),
    )

    result = service.export(
        format_name="csv",
        filters=ExportFilters(title_query="Python", limit=100, offset=0),
    )

    csv_text = result.artifact.content.decode("utf-8")
    assert "Python Engineer" in csv_text
    assert "Frontend Engineer" not in csv_text
    assert "applied" in csv_text
