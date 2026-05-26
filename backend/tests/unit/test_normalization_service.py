from __future__ import annotations

from datetime import datetime, timezone

from app.db.models.job_source import JobSource
from app.scrapers.contracts import ScrapedRecord
from app.services.normalization_service import NormalizationService


def test_normalization_extracts_expected_fields() -> None:
    service = NormalizationService()
    source = JobSource(name="GH", base_url="https://jobs.example.com", profile_id=1, enabled=True, config={})
    record = ScrapedRecord(
        external_ref="job-1",
        raw_payload={
            "title": "Senior Python Engineer",
            "company": "Acme",
            "location": "Remote",
            "work_mode": "Remote",
            "employment_type": "Full-time",
            "posted_at": "2026-01-01T00:00:00Z",
            "apply_url": "https://jobs.example.com/job-1",
            "description": "Build APIs",
            "tags": ["backend", "python"],
            "skills": ["Python", "FastAPI"],
        },
        source_snapshot=None,
        scraped_at=datetime.now(timezone.utc),
    )

    normalized = service.normalize("greenhouse", source, record)

    assert normalized.title == "Senior Python Engineer"
    assert normalized.company == "Acme"
    assert normalized.location == "Remote"
    assert normalized.work_mode == "remote"
    assert normalized.employment_type == "Full-time"
    assert normalized.posted_at is not None
    assert normalized.posted_at.tzinfo is not None
    assert normalized.apply_url == "https://jobs.example.com/job-1"
    assert normalized.description_snippet == "Build APIs"
    assert normalized.tags == ["backend", "python"]
    assert normalized.skills == ["Python", "FastAPI"]


def test_normalization_fallbacks_are_deterministic() -> None:
    service = NormalizationService()
    source = JobSource(name="Fallback", base_url="https://fallback.example.com", profile_id=1, enabled=True, config={})
    record = ScrapedRecord(
        external_ref=None,
        raw_payload={},
        source_snapshot=None,
        scraped_at=datetime.now(timezone.utc),
    )

    normalized = service.normalize("custom-html", source, record)

    assert normalized.title == "Unknown Title"
    assert normalized.company == "Unknown Company"
    assert normalized.apply_url == "https://fallback.example.com"
    assert normalized.tags == []
    assert normalized.skills == []


def test_normalization_extracts_greenhouse_object_location() -> None:
    service = NormalizationService()
    source = JobSource(name="GH", base_url="https://jobs.example.com", profile_id=1, enabled=True, config={})
    record = ScrapedRecord(
        external_ref="job-2",
        raw_payload={
            "title": "Platform Engineer",
            "company": "Acme",
            "location": {"name": "San Francisco, CA"},
            "absolute_url": "https://boards.greenhouse.io/acme/jobs/2",
        },
        source_snapshot=None,
        scraped_at=datetime.now(timezone.utc),
    )

    normalized = service.normalize("greenhouse", source, record)

    assert normalized.location == "San Francisco, CA"


def test_normalization_extracts_greenhouse_work_mode_from_metadata() -> None:
    service = NormalizationService()
    source = JobSource(name="GH", base_url="https://jobs.example.com", profile_id=1, enabled=True, config={})
    record = ScrapedRecord(
        external_ref="job-3",
        raw_payload={
            "title": "Account Executive",
            "company": "Anthropic",
            "metadata": [
                {
                    "name": "Location Type",
                    "value": "On-Site",
                }
            ],
        },
        source_snapshot=None,
        scraped_at=datetime.now(timezone.utc),
    )

    normalized = service.normalize("greenhouse", source, record)

    assert normalized.work_mode == "onsite"
