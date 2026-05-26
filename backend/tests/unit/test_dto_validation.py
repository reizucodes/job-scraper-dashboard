from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.bookmark import JobBookmarkUpsert
from app.schemas.job_source import JobSourceCreate


def test_job_source_create_validates_url() -> None:
    dto = JobSourceCreate(
        name="Main Source",
        base_url="https://jobs.example.com",
        profile_id=1,
        enabled=True,
        config={},
    )

    assert dto.base_url.host == "jobs.example.com"


def test_job_source_create_rejects_invalid_url() -> None:
    with pytest.raises(ValidationError):
        JobSourceCreate(
            name="Main Source",
            base_url="not-a-url",
            profile_id=1,
            enabled=True,
            config={},
        )


def test_bookmark_status_accepts_known_enum_value() -> None:
    dto = JobBookmarkUpsert(status="applied", notes="Submitted")
    assert dto.status.value == "applied"


def test_bookmark_status_rejects_unknown_value() -> None:
    with pytest.raises(ValidationError):
        JobBookmarkUpsert(status="maybe", notes="N/A")


def test_datetime_fields_keep_timezone() -> None:
    now = datetime.now(timezone.utc)
    dto = JobBookmarkUpsert(status="new", notes=now.isoformat())
    assert dto.status.value == "new"
