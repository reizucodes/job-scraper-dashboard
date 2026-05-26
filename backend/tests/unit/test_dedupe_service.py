from __future__ import annotations

from datetime import datetime, timezone

from app.db.models.job_source import JobSource
from app.db.models.source_profile import SourceProfile
from app.repositories.job_listing_repo import SQLAlchemyJobListingRepository
from app.services.dedupe_service import DedupeService
from app.services.normalization_service import NormalizedJobData


def _normalized(apply_url: str, title: str = "Python Engineer") -> NormalizedJobData:
    return NormalizedJobData(
        title=title,
        company="Acme",
        location="Remote",
        work_mode="remote",
        employment_type="full-time",
        posted_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        apply_url=apply_url,
        description_snippet="Build APIs",
        tags=["backend"],
        skills=["Python"],
    )


def _seed_source(db_session):
    profile = SourceProfile(code="greenhouse", display_name="Greenhouse", active=True)
    db_session.add(profile)
    db_session.commit()
    source = JobSource(
        name="Source",
        base_url="https://jobs.example.com",
        profile_id=profile.id,
        enabled=True,
        config={},
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)
    return source


def test_canonical_key_prefers_external_ref(db_session) -> None:
    service = DedupeService(SQLAlchemyJobListingRepository(db_session))

    key_1 = service.generate_canonical_key(
        source_id=1,
        external_ref="ABC-123",
        apply_url="https://jobs.example.com/a",
        title="T",
        company="C",
        location="L",
    )
    key_2 = service.generate_canonical_key(
        source_id=1,
        external_ref="abc-123",
        apply_url="https://jobs.example.com/b",
        title="T2",
        company="C2",
        location="L2",
    )
    assert key_1 == key_2


def test_canonical_key_fallbacks(db_session) -> None:
    service = DedupeService(SQLAlchemyJobListingRepository(db_session))

    key_url = service.generate_canonical_key(
        source_id=1,
        external_ref=None,
        apply_url="https://jobs.example.com/x",
        title="T",
        company="C",
        location="L",
    )
    key_fallback = service.generate_canonical_key(
        source_id=1,
        external_ref=None,
        apply_url=None,
        title="T",
        company="C",
        location="L",
    )
    assert key_url.startswith("src:1:url:")
    assert key_fallback.startswith("src:1:fallback:")


def test_dedupe_insert_update_duplicate(db_session) -> None:
    source = _seed_source(db_session)
    repo = SQLAlchemyJobListingRepository(db_session)
    service = DedupeService(repo)
    seen_at = datetime.now(timezone.utc)

    class Raw:
        id = 1

    canonical = service.generate_canonical_key(
        source_id=source.id,
        external_ref="job-1",
        apply_url="https://jobs.example.com/1",
        title="Python Engineer",
        company="Acme",
        location="Remote",
    )

    inserted = service.upsert_listing(
        source_id=source.id,
        raw_job=Raw(),
        normalized=_normalized("https://jobs.example.com/1", "Python Engineer"),
        canonical_key=canonical,
        seen_at=seen_at,
    )
    assert inserted.action == "inserted"

    class Raw2:
        id = 2

    duplicate = service.upsert_listing(
        source_id=source.id,
        raw_job=Raw2(),
        normalized=_normalized("https://jobs.example.com/1", "Python Engineer"),
        canonical_key=canonical,
        seen_at=seen_at,
    )
    assert duplicate.action == "duplicate"

    class Raw3:
        id = 3

    updated = service.upsert_listing(
        source_id=source.id,
        raw_job=Raw3(),
        normalized=_normalized("https://jobs.example.com/1", "Senior Python Engineer"),
        canonical_key=canonical,
        seen_at=seen_at,
    )
    assert updated.action == "updated"
    assert updated.listing.title == "Senior Python Engineer"
