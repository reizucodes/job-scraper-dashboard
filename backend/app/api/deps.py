from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exporters import CsvExporter, ExporterRegistry, XlsxExporter
from app.repositories.job_bookmark_repo import SQLAlchemyJobBookmarkRepository
from app.repositories.job_listing_repo import SQLAlchemyJobListingRepository
from app.repositories.job_source_repo import SQLAlchemyJobSourceRepository
from app.repositories.raw_job_repo import SQLAlchemyRawJobRepository
from app.repositories.scrape_run_repo import SQLAlchemyScrapeRunRepository
from app.repositories.source_profile_repo import SQLAlchemySourceProfileRepository
from app.scrapers.profiles import CustomHtmlScraperAdapter, GreenhouseScraperAdapter, LeverScraperAdapter
from app.scrapers.registry import ScraperRegistry
from app.services.dedupe_service import DedupeService
from app.services.export_service import ExportService
from app.services.job_bookmark_service import JobBookmarkService
from app.services.job_listing_service import JobListingService
from app.services.job_source_service import JobSourceService
from app.services.normalization_service import NormalizationService
from app.services.scrape_run_service import ScrapeRunService
from app.services.source_profile_service import SourceProfileService


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_scraper_registry() -> ScraperRegistry:
    return ScraperRegistry(
        adapters=[
            GreenhouseScraperAdapter(),
            LeverScraperAdapter(),
            CustomHtmlScraperAdapter(),
        ]
    )


def get_exporter_registry() -> ExporterRegistry:
    return ExporterRegistry(exporters=[CsvExporter(), XlsxExporter()])


def get_source_profile_service(session: Session = Depends(get_db_session)) -> SourceProfileService:
    repository = SQLAlchemySourceProfileRepository(session)
    return SourceProfileService(repository=repository)


def get_job_source_service(session: Session = Depends(get_db_session)) -> JobSourceService:
    source_repo = SQLAlchemyJobSourceRepository(session)
    profile_repo = SQLAlchemySourceProfileRepository(session)
    return JobSourceService(session=session, source_repository=source_repo, profile_repository=profile_repo)


def get_scrape_run_service(
    session: Session = Depends(get_db_session),
    scraper_registry: ScraperRegistry = Depends(get_scraper_registry),
) -> ScrapeRunService:
    run_repo = SQLAlchemyScrapeRunRepository(session)
    source_repo = SQLAlchemyJobSourceRepository(session)
    profile_repo = SQLAlchemySourceProfileRepository(session)
    raw_job_repo = SQLAlchemyRawJobRepository(session)
    listing_repo = SQLAlchemyJobListingRepository(session)
    return ScrapeRunService(
        session=session,
        run_repository=run_repo,
        source_repository=source_repo,
        profile_repository=profile_repo,
        raw_job_repository=raw_job_repo,
        scraper_registry=scraper_registry,
        normalization_service=NormalizationService(),
        dedupe_service=DedupeService(listing_repository=listing_repo),
    )


def get_job_listing_service(session: Session = Depends(get_db_session)) -> JobListingService:
    listing_repository = SQLAlchemyJobListingRepository(session)
    bookmark_repository = SQLAlchemyJobBookmarkRepository(session)
    return JobListingService(repository=listing_repository, bookmark_repository=bookmark_repository)


def get_job_bookmark_service(session: Session = Depends(get_db_session)) -> JobBookmarkService:
    bookmark_repo = SQLAlchemyJobBookmarkRepository(session)
    listing_repo = SQLAlchemyJobListingRepository(session)
    return JobBookmarkService(session=session, bookmark_repository=bookmark_repo, listing_repository=listing_repo)


def get_export_service(
    session: Session = Depends(get_db_session),
    exporter_registry: ExporterRegistry = Depends(get_exporter_registry),
) -> ExportService:
    listing_repo = SQLAlchemyJobListingRepository(session)
    bookmark_repo = SQLAlchemyJobBookmarkRepository(session)
    return ExportService(listing_repository=listing_repo, bookmark_repository=bookmark_repo, exporter_registry=exporter_registry)
