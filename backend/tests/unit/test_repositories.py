from datetime import datetime, timezone

from app.db.models.job_bookmark import JobBookmark
from app.db.models.job_listing import JobListing
from app.db.models.job_source import JobSource
from app.db.models.raw_job import RawJob
from app.db.models.scrape_run import ScrapeRun
from app.db.models.source_profile import SourceProfile
from app.repositories import (
    JobListingFilters,
    SQLAlchemyJobBookmarkRepository,
    SQLAlchemyJobListingRepository,
    SQLAlchemyJobSourceRepository,
    SQLAlchemyRawJobRepository,
    SQLAlchemyScrapeRunRepository,
    SQLAlchemySourceProfileRepository,
)


def _seed_profile(db_session) -> SourceProfile:
    profile = SourceProfile(code="greenhouse", display_name="Greenhouse", active=True)
    db_session.add(profile)
    db_session.flush()
    return profile


def _seed_source(db_session, profile_id: int) -> JobSource:
    source = JobSource(
        name="Primary",
        base_url="https://jobs.example.com",
        profile_id=profile_id,
        enabled=True,
        config={},
    )
    db_session.add(source)
    db_session.flush()
    return source


def test_source_profile_repository_list_and_get(db_session) -> None:
    _seed_profile(db_session)
    repo = SQLAlchemySourceProfileRepository(db_session)

    profiles = repo.list_active()
    assert len(profiles) == 1
    assert repo.get_by_code("greenhouse") is not None


def test_job_source_repository_crud(db_session) -> None:
    profile = _seed_profile(db_session)
    repo = SQLAlchemyJobSourceRepository(db_session)

    created = repo.create(
        JobSource(
            name="Source A",
            base_url="https://jobs.a.com",
            profile_id=profile.id,
            enabled=True,
            config={"department": "eng"},
        )
    )
    assert created.id is not None

    loaded = repo.get(created.id)
    assert loaded is not None
    assert loaded.name == "Source A"

    loaded.enabled = False
    updated = repo.update(loaded)
    assert updated.enabled is False

    assert repo.delete(created.id) is True
    assert repo.get(created.id) is None


def test_scrape_raw_listing_and_bookmark_repositories(db_session) -> None:
    profile = _seed_profile(db_session)
    source = _seed_source(db_session, profile.id)

    run_repo = SQLAlchemyScrapeRunRepository(db_session)
    raw_repo = SQLAlchemyRawJobRepository(db_session)
    listing_repo = SQLAlchemyJobListingRepository(db_session)
    bookmark_repo = SQLAlchemyJobBookmarkRepository(db_session)

    run = run_repo.create(
        ScrapeRun(
            source_id=source.id,
            status="completed",
            started_at=datetime.now(timezone.utc),
            ended_at=datetime.now(timezone.utc),
            duration_ms=100,
        )
    )

    raw = raw_repo.create(
        RawJob(
            source_id=source.id,
            scrape_run_id=run.id,
            external_ref="job-1",
            source_snapshot="<html></html>",
            raw_payload={"id": "job-1"},
            payload_hash="abc123",
            scraped_at=datetime.now(timezone.utc),
        )
    )

    listing = listing_repo.create(
        JobListing(
            source_id=source.id,
            raw_job_id=raw.id,
            canonical_key="greenhouse:job-1",
            title="Python Engineer",
            company="Example",
            location="San Francisco, CA | New York City, NY",
            work_mode="hybrid (travel-required)",
            employment_type="full-time",
            apply_url="https://jobs.example.com/job-1",
            tags=["backend"],
            skills=["Python"],
            first_seen_at=datetime.now(timezone.utc),
            last_seen_at=datetime.now(timezone.utc),
            is_active=True,
        )
    )

    filtered = listing_repo.list_filtered(JobListingFilters(title_query="Python"))
    assert len(filtered) == 1
    assert filtered[0].id == listing.id

    mode_filtered = listing_repo.list_filtered(JobListingFilters(work_mode="hybrid"))
    assert len(mode_filtered) == 1
    assert mode_filtered[0].id == listing.id

    location_filtered = listing_repo.list_filtered(JobListingFilters(location="CA"))
    assert len(location_filtered) == 1
    assert location_filtered[0].id == listing.id

    upserted = bookmark_repo.upsert(
        JobBookmark(
            job_id=listing.id,
            status="interested",
            notes="Strong fit",
            updated_at=datetime.now(timezone.utc),
        )
    )
    assert upserted.status == "interested"

    loaded_bookmark = bookmark_repo.get_by_job_id(listing.id)
    assert loaded_bookmark is not None
    assert loaded_bookmark.notes == "Strong fit"
