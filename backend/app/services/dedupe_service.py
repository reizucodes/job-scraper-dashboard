from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone

from app.db.models.job_listing import JobListing
from app.db.models.raw_job import RawJob
from app.repositories.interfaces import JobListingRepository
from app.services.normalization_service import NormalizedJobData


@dataclass(slots=True)
class DedupeUpsertResult:
    action: str  # inserted | updated | duplicate
    listing: JobListing


class DedupeService:
    def __init__(self, listing_repository: JobListingRepository) -> None:
        self._listing_repository = listing_repository

    def generate_canonical_key(
        self,
        *,
        source_id: int,
        external_ref: str | None,
        apply_url: str | None,
        title: str,
        company: str,
        location: str | None,
    ) -> str:
        if external_ref:
            return f"src:{source_id}:ext:{self._hash(external_ref.strip().lower())}"

        if apply_url:
            return f"src:{source_id}:url:{self._hash(apply_url.strip().lower())}"

        fallback = "|".join(
            [
                title.strip().lower(),
                company.strip().lower(),
                (location or "").strip().lower(),
            ]
        )
        return f"src:{source_id}:fallback:{self._hash(fallback)}"

    def upsert_listing(
        self,
        *,
        source_id: int,
        raw_job: RawJob,
        normalized: NormalizedJobData,
        canonical_key: str,
        seen_at: datetime,
    ) -> DedupeUpsertResult:
        existing = self._listing_repository.get_by_canonical_key(canonical_key)
        if existing is None:
            listing = self._listing_repository.create(
                JobListing(
                    source_id=source_id,
                    raw_job_id=raw_job.id,
                    canonical_key=canonical_key,
                    title=normalized.title,
                    company=normalized.company,
                    location=normalized.location,
                    work_mode=normalized.work_mode,
                    employment_type=normalized.employment_type,
                    posted_at=normalized.posted_at,
                    apply_url=normalized.apply_url,
                    description_snippet=normalized.description_snippet,
                    tags=normalized.tags,
                    skills=normalized.skills,
                    first_seen_at=seen_at,
                    last_seen_at=seen_at,
                    is_active=True,
                )
            )
            return DedupeUpsertResult(action="inserted", listing=listing)

        changed = self._apply_changes(existing, normalized)
        existing.raw_job_id = raw_job.id
        existing.last_seen_at = seen_at

        updated = self._listing_repository.update(existing)
        if changed:
            return DedupeUpsertResult(action="updated", listing=updated)
        return DedupeUpsertResult(action="duplicate", listing=updated)

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _apply_changes(existing: JobListing, normalized: NormalizedJobData) -> bool:
        changed = False

        field_pairs = [
            ("title", normalized.title),
            ("company", normalized.company),
            ("location", normalized.location),
            ("work_mode", normalized.work_mode),
            ("employment_type", normalized.employment_type),
            ("posted_at", normalized.posted_at),
            ("apply_url", normalized.apply_url),
            ("description_snippet", normalized.description_snippet),
            ("tags", normalized.tags),
            ("skills", normalized.skills),
        ]

        for field_name, incoming in field_pairs:
            current = getattr(existing, field_name)
            if not DedupeService._field_equals(current, incoming):
                setattr(existing, field_name, incoming)
                changed = True

        return changed

    @staticmethod
    def _field_equals(current: object, incoming: object) -> bool:
        if isinstance(current, datetime) or isinstance(incoming, datetime):
            current_dt = DedupeService._normalize_datetime(current)
            incoming_dt = DedupeService._normalize_datetime(incoming)
            return current_dt == incoming_dt
        return current == incoming

    @staticmethod
    def _normalize_datetime(value: object) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, datetime):
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
