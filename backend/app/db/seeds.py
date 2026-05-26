from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import utcnow
from app.db.models.enums import SourceProfileCode
from app.db.models.job_source import JobSource
from app.db.models.source_profile import SourceProfile

DEFAULT_SOURCE_PROFILES: tuple[tuple[str, str], ...] = (
    (SourceProfileCode.GREENHOUSE.value, "Greenhouse"),
    (SourceProfileCode.LEVER.value, "Lever"),
    (SourceProfileCode.CUSTOM_HTML.value, "Custom HTML"),
)

DEFAULT_JOB_SOURCES: tuple[dict[str, object], ...] = (
    {
        "name": "Anthropic",
        "base_url": "https://www.anthropic.com/careers",
        "profile_code": SourceProfileCode.GREENHOUSE.value,
        "config": {
            "mode": "live",
            "jobs_url": "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs",
        },
    },
    {
        "name": "Stripe",
        "base_url": "https://stripe.com/jobs",
        "profile_code": SourceProfileCode.GREENHOUSE.value,
        "config": {
            "mode": "live",
            "jobs_url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs",
        },
    },
)


def seed_source_profiles(session: Session) -> None:
    existing_codes = {
        row[0]
        for row in session.execute(select(SourceProfile.code)).all()
    }

    now = utcnow()
    for code, display_name in DEFAULT_SOURCE_PROFILES:
        if code in existing_codes:
            continue
        session.add(
            SourceProfile(
                code=code,
                display_name=display_name,
                active=True,
                created_at=now,
                updated_at=now,
            )
        )
    session.flush()


def seed_job_sources(session: Session) -> None:
    existing_count = session.scalar(select(JobSource.id).limit(1))
    if existing_count is not None:
        return

    profiles_by_code = {
        profile.code: profile
        for profile in session.scalars(select(SourceProfile)).all()
    }
    greenhouse = profiles_by_code.get(SourceProfileCode.GREENHOUSE.value)
    if greenhouse is None:
        raise RuntimeError("Greenhouse source profile must exist before seeding job sources")

    now = utcnow()
    for payload in DEFAULT_JOB_SOURCES:
        session.add(
            JobSource(
                name=str(payload["name"]),
                base_url=str(payload["base_url"]),
                profile_id=greenhouse.id,
                enabled=True,
                config=dict(payload["config"]),
                created_at=now,
                updated_at=now,
            )
        )
    session.flush()
