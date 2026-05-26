from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.job_source import JobSource
from app.db.models.raw_job import RawJob
from app.db.models.scrape_run import ScrapeRun
from app.repositories.interfaces import JobSourceRepository, RawJobRepository, ScrapeRunRepository, SourceProfileRepository
from app.scrapers.registry import ScraperRegistry
from app.services.dedupe_service import DedupeService
from app.services.errors import NotFoundError
from app.services.normalization_service import NormalizationService


@dataclass(slots=True)
class ScrapeRunExecutionResult:
    run: ScrapeRun


class ScrapeRunService:
    def __init__(
        self,
        session: Session,
        run_repository: ScrapeRunRepository,
        source_repository: JobSourceRepository,
        profile_repository: SourceProfileRepository,
        raw_job_repository: RawJobRepository,
        scraper_registry: ScraperRegistry,
        normalization_service: NormalizationService,
        dedupe_service: DedupeService,
    ) -> None:
        self._session = session
        self._run_repository = run_repository
        self._source_repository = source_repository
        self._profile_repository = profile_repository
        self._raw_job_repository = raw_job_repository
        self._scraper_registry = scraper_registry
        self._normalization_service = normalization_service
        self._dedupe_service = dedupe_service

    def list_runs(self, limit: int = 50) -> list[ScrapeRun]:
        return self._run_repository.list_recent(limit=limit)

    def get_run(self, run_id: int) -> ScrapeRun:
        run = self._run_repository.get(run_id)
        if run is None:
            raise NotFoundError(f"Scrape run {run_id} not found")
        return run

    def trigger_run(self, source_ids: list[int] | None) -> ScrapeRunExecutionResult:
        started_at = datetime.now(timezone.utc)
        run = self._run_repository.create(
            ScrapeRun(
                source_id=None,
                status="running",
                started_at=started_at,
                records_seen=0,
                records_inserted=0,
                records_updated=0,
                duplicates=0,
                failures=0,
            )
        )

        failures: list[str] = []
        sources = self._resolve_sources(source_ids=source_ids, run=run, failures=failures)

        for source in sources:
            profile = self._profile_repository.get(source.profile_id)
            if profile is None:
                run.failures += 1
                failures.append(f"source:{source.id} profile:{source.profile_id} missing")
                continue

            try:
                adapter = self._scraper_registry.get(profile.code)
                scraped_records = adapter.scrape(source)
            except Exception as exc:  # noqa: BLE001
                run.failures += 1
                failures.append(f"source:{source.id} adapter error: {exc}")
                continue

            run.records_seen += len(scraped_records)

            for record in scraped_records:
                payload_hash = self._hash_payload(record.raw_payload)
                raw_job = self._raw_job_repository.create(
                    RawJob(
                        source_id=source.id,
                        scrape_run_id=run.id,
                        external_ref=record.external_ref,
                        source_snapshot=record.source_snapshot,
                        raw_payload=record.raw_payload,
                        payload_hash=payload_hash,
                        scraped_at=record.scraped_at,
                    )
                )
                normalized = self._normalization_service.normalize(profile.code, source, record)
                canonical_key = self._dedupe_service.generate_canonical_key(
                    source_id=source.id,
                    external_ref=record.external_ref,
                    apply_url=normalized.apply_url,
                    title=normalized.title,
                    company=normalized.company,
                    location=normalized.location,
                )
                upsert_result = self._dedupe_service.upsert_listing(
                    source_id=source.id,
                    raw_job=raw_job,
                    normalized=normalized,
                    canonical_key=canonical_key,
                    seen_at=record.scraped_at,
                )
                if upsert_result.action == "inserted":
                    run.records_inserted += 1
                elif upsert_result.action == "updated":
                    run.records_updated += 1
                else:
                    run.duplicates += 1

        finished_at = datetime.now(timezone.utc)
        run.ended_at = finished_at
        run.duration_ms = max(0, int((finished_at - started_at).total_seconds() * 1000))
        if run.failures > 0:
            run.status = "failed"
            run.error_summary = "; ".join(failures)
        else:
            run.status = "completed"
            run.error_summary = None

        updated = self._run_repository.update(run)
        self._session.commit()
        self._session.refresh(updated)
        return ScrapeRunExecutionResult(run=updated)

    def _resolve_sources(self, source_ids: list[int] | None, run: ScrapeRun, failures: list[str]) -> list[JobSource]:
        if not source_ids:
            return self._source_repository.list_enabled()

        resolved_sources = self._source_repository.list_by_ids(source_ids)
        resolved_by_id = {source.id: source for source in resolved_sources}
        missing_source_ids = [source_id for source_id in source_ids if source_id not in resolved_by_id]
        disabled_source_ids = [source_id for source_id in source_ids if source_id in resolved_by_id and not resolved_by_id[source_id].enabled]

        for source_id in missing_source_ids:
            run.failures += 1
            failures.append(f"source:{source_id} missing")
        for source_id in disabled_source_ids:
            run.failures += 1
            failures.append(f"source:{source_id} disabled")

        return [source for source in resolved_sources if source.enabled]

    @staticmethod
    def _hash_payload(payload: dict[str, object]) -> str:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
