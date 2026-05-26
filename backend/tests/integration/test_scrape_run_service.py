from __future__ import annotations

from sqlalchemy import select

from app.db.models.job_source import JobSource
from app.db.models.job_listing import JobListing
from app.db.models.raw_job import RawJob
from app.db.models.source_profile import SourceProfile
from app.repositories.job_listing_repo import SQLAlchemyJobListingRepository
from app.repositories.job_source_repo import SQLAlchemyJobSourceRepository
from app.repositories.raw_job_repo import SQLAlchemyRawJobRepository
from app.repositories.scrape_run_repo import SQLAlchemyScrapeRunRepository
from app.repositories.source_profile_repo import SQLAlchemySourceProfileRepository
from app.scrapers.profiles import GreenhouseScraperAdapter
from app.scrapers.registry import ScraperRegistry
from app.services.dedupe_service import DedupeService
from app.services.normalization_service import NormalizationService
from app.services.scrape_run_service import ScrapeRunService


def _create_profile(db_session, code: str, name: str) -> SourceProfile:
    profile = SourceProfile(code=code, display_name=name, active=True)
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def test_scrape_run_service_persists_raw_jobs_and_metrics(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    source = JobSource(
        name="GH Source",
        base_url="https://boards.greenhouse.io/example",
        profile_id=profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1", "title": "Python"}, {"id": "job-2", "title": "Vue"}]},
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    result = service.trigger_run(source_ids=[source.id])

    assert result.run.status == "completed"
    assert result.run.records_seen == 2
    assert result.run.records_inserted == 2
    assert result.run.records_updated == 0
    assert result.run.duplicates == 0
    assert result.run.failures == 0
    assert result.run.duration_ms is not None

    raw_jobs = list(db_session.scalars(select(RawJob).where(RawJob.scrape_run_id == result.run.id)).all())
    assert len(raw_jobs) == 2
    listings = list(db_session.scalars(select(JobListing).order_by(JobListing.id.asc())).all())
    assert len(listings) == 2


def test_scrape_run_service_marks_failed_when_adapter_missing(db_session) -> None:
    missing_profile = _create_profile(db_session, "workday", "Workday")
    source = JobSource(
        name="Workday Source",
        base_url="https://company.workdayjobs.com",
        profile_id=missing_profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1"}]},
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    result = service.trigger_run(source_ids=None)

    assert result.run.status == "failed"
    assert result.run.records_seen == 0
    assert result.run.records_inserted == 0
    assert result.run.failures == 1


def test_scrape_run_service_repeated_scrape_marks_duplicates(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    source = JobSource(
        name="GH Source",
        base_url="https://boards.greenhouse.io/example",
        profile_id=profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1", "title": "Python"}]},
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    first = service.trigger_run(source_ids=[source.id])
    second = service.trigger_run(source_ids=[source.id])

    assert first.run.records_inserted == 1
    assert second.run.records_inserted == 0
    assert second.run.duplicates == 1

    listings = list(db_session.scalars(select(JobListing)).all())
    assert len(listings) == 1


def test_scrape_run_service_persists_location_from_greenhouse_object_payload(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    source = JobSource(
        name="GH Source Location",
        base_url="https://boards.greenhouse.io/example",
        profile_id=profile.id,
        enabled=True,
        config={
            "fixtures": [
                {
                    "id": "job-location-1",
                    "title": "Backend Engineer",
                    "location": {"name": "Remote - US"},
                }
            ]
        },
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    result = service.trigger_run(source_ids=[source.id])

    assert result.run.status == "completed"
    listing = db_session.scalars(select(JobListing).where(JobListing.source_id == source.id)).one()
    assert listing.location == "Remote - US"


def test_scrape_run_service_persists_greenhouse_work_mode_from_metadata(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    source = JobSource(
        name="GH Source Mode",
        base_url="https://boards.greenhouse.io/example",
        profile_id=profile.id,
        enabled=True,
        config={
            "fixtures": [
                {
                    "id": "job-mode-1",
                    "title": "Account Executive",
                    "metadata": [
                        {
                            "name": "Location Type",
                            "value": "On-Site",
                        }
                    ],
                }
            ]
        },
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    result = service.trigger_run(source_ids=[source.id])

    assert result.run.status == "completed"
    listing = db_session.scalars(select(JobListing).where(JobListing.source_id == source.id)).one()
    assert listing.work_mode == "onsite"


def test_scrape_run_service_all_enabled_only(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    enabled_source = JobSource(
        name="Enabled Source",
        base_url="https://boards.greenhouse.io/enabled",
        profile_id=profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-enabled-1", "title": "Python"}]},
    )
    disabled_source = JobSource(
        name="Disabled Source",
        base_url="https://boards.greenhouse.io/disabled",
        profile_id=profile.id,
        enabled=False,
        config={"fixtures": [{"id": "job-disabled-1", "title": "Rust"}]},
    )
    db_session.add_all([enabled_source, disabled_source])
    db_session.commit()
    db_session.refresh(enabled_source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    result = service.trigger_run(source_ids=None)

    assert result.run.status == "completed"
    assert result.run.records_seen == 1
    assert result.run.failures == 0
    listings = list(db_session.scalars(select(JobListing).order_by(JobListing.id.asc())).all())
    assert len(listings) == 1
    assert listings[0].source_id == enabled_source.id


def test_scrape_run_service_selected_source_respects_enabled_flag(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    enabled_source = JobSource(
        name="Enabled Source",
        base_url="https://boards.greenhouse.io/enabled",
        profile_id=profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-enabled-1", "title": "Python"}]},
    )
    disabled_source = JobSource(
        name="Disabled Source",
        base_url="https://boards.greenhouse.io/disabled",
        profile_id=profile.id,
        enabled=False,
        config={"fixtures": [{"id": "job-disabled-1", "title": "Rust"}]},
    )
    db_session.add_all([enabled_source, disabled_source])
    db_session.commit()
    db_session.refresh(enabled_source)
    db_session.refresh(disabled_source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    enabled_only = service.trigger_run(source_ids=[enabled_source.id])
    assert enabled_only.run.status == "completed"
    assert enabled_only.run.records_seen == 1
    assert enabled_only.run.failures == 0

    mixed = service.trigger_run(source_ids=[enabled_source.id, disabled_source.id])
    assert mixed.run.status == "failed"
    assert mixed.run.records_seen == 1
    assert mixed.run.failures == 1
    assert mixed.run.error_summary is not None
    assert f"source:{disabled_source.id} disabled" in mixed.run.error_summary


def test_scrape_run_service_missing_source_ids_are_reported(db_session) -> None:
    profile = _create_profile(db_session, "greenhouse", "Greenhouse")
    source = JobSource(
        name="Enabled Source",
        base_url="https://boards.greenhouse.io/enabled",
        profile_id=profile.id,
        enabled=True,
        config={"fixtures": [{"id": "job-enabled-1", "title": "Python"}]},
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)

    service = ScrapeRunService(
        session=db_session,
        run_repository=SQLAlchemyScrapeRunRepository(db_session),
        source_repository=SQLAlchemyJobSourceRepository(db_session),
        profile_repository=SQLAlchemySourceProfileRepository(db_session),
        raw_job_repository=SQLAlchemyRawJobRepository(db_session),
        scraper_registry=ScraperRegistry(adapters=[GreenhouseScraperAdapter()]),
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(SQLAlchemyJobListingRepository(db_session)),
    )

    all_valid = service.trigger_run(source_ids=[source.id])
    assert all_valid.run.status == "completed"
    assert all_valid.run.failures == 0

    some_missing = service.trigger_run(source_ids=[source.id, 999001])
    assert some_missing.run.status == "failed"
    assert some_missing.run.records_seen == 1
    assert some_missing.run.failures == 1
    assert some_missing.run.error_summary is not None
    assert "source:999001 missing" in some_missing.run.error_summary

    all_missing = service.trigger_run(source_ids=[999101, 999102])
    assert all_missing.run.status == "failed"
    assert all_missing.run.records_seen == 0
    assert all_missing.run.failures == 2
    assert all_missing.run.error_summary is not None
    assert "source:999101 missing" in all_missing.run.error_summary
    assert "source:999102 missing" in all_missing.run.error_summary
