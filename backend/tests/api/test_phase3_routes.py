from __future__ import annotations

import csv
import io
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.job_bookmark import JobBookmark
from app.db.models.job_listing import JobListing
from app.db.models.job_source import JobSource
from app.db.models.raw_job import RawJob
from app.db.models.scrape_run import ScrapeRun
from app.db.models.source_profile import SourceProfile
from app.db.seeds import seed_source_profiles


def _seed_profiles(api_db_session: Session) -> list[SourceProfile]:
    seed_source_profiles(api_db_session)
    api_db_session.commit()
    return list(api_db_session.scalars(select(SourceProfile).order_by(SourceProfile.code.asc())).all())


def _seed_source(api_db_session: Session, profile_id: int) -> JobSource:
    source = JobSource(
        name="Primary Source",
        base_url="https://jobs.example.com",
        profile_id=profile_id,
        enabled=True,
        config={},
    )
    api_db_session.add(source)
    api_db_session.commit()
    api_db_session.refresh(source)
    return source


def test_get_source_profiles(api_client, api_db_session: Session) -> None:
    _seed_profiles(api_db_session)

    response = api_client.get("/source-profiles")

    assert response.status_code == 200
    payload = response.json()
    assert [item["code"] for item in payload] == ["custom-html", "greenhouse", "lever"]


def test_job_source_crud(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")

    create_response = api_client.post(
        "/job-sources",
        json={
            "name": "Greenhouse Source",
            "base_url": "https://boards.greenhouse.io/example",
            "profile_id": greenhouse.id,
            "enabled": True,
            "config": {"department": "Engineering"},
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()

    list_response = api_client.get("/job-sources")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    patch_response = api_client.patch(
        f"/job-sources/{created['id']}",
        json={"enabled": False},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["enabled"] is False

    delete_response = api_client.delete(f"/job-sources/{created['id']}")
    assert delete_response.status_code == 204

    list_after_delete = api_client.get("/job-sources")
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []


def test_job_source_create_404_when_profile_missing(api_client) -> None:
    response = api_client.post(
        "/job-sources",
        json={
            "name": "Invalid Source",
            "base_url": "https://jobs.example.com",
            "profile_id": 9999,
            "enabled": True,
            "config": {},
        },
    )

    assert response.status_code == 404


def test_job_source_create_rejects_invalid_mode(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    response = api_client.post(
        "/job-sources",
        json={
            "name": "Invalid Mode Source",
            "base_url": "https://boards.greenhouse.io/example",
            "profile_id": greenhouse.id,
            "enabled": True,
            "config": {"mode": "bad-mode"},
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid job source config"


def test_job_source_create_rejects_live_mode_missing_jobs_url(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    response = api_client.post(
        "/job-sources",
        json={
            "name": "Missing Jobs URL",
            "base_url": "https://boards.greenhouse.io/example",
            "profile_id": greenhouse.id,
            "enabled": True,
            "config": {"mode": "live"},
        },
    )

    assert response.status_code == 422
    assert "config.jobs_url is required for live mode" in response.json()["errors"]


def test_job_source_create_rejects_live_mode_invalid_jobs_url(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    lever = next(profile for profile in profiles if profile.code == "lever")
    response = api_client.post(
        "/job-sources",
        json={
            "name": "Bad Lever URL",
            "base_url": "https://api.lever.co",
            "profile_id": lever.id,
            "enabled": True,
            "config": {"mode": "live", "jobs_url": "invalid-url"},
        },
    )

    assert response.status_code == 422
    assert "config.jobs_url must be a valid URL" in response.json()["errors"]


def test_job_source_update_rejects_invalid_timeout(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = _seed_source(api_db_session, greenhouse.id)
    response = api_client.patch(f"/job-sources/{source.id}", json={"config": {"mode": "fixture", "timeout_seconds": 0}})

    assert response.status_code == 422
    assert "config.timeout_seconds must be between 1 and 30" in response.json()["errors"]


def test_job_source_create_accepts_valid_fixture_mode(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    response = api_client.post(
        "/job-sources",
        json={
            "name": "Fixture Source",
            "base_url": "https://boards.greenhouse.io/example",
            "profile_id": greenhouse.id,
            "enabled": True,
            "config": {"mode": "fixture", "fixtures": [{"id": "job-1"}]},
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["config"]["mode"] == "fixture"


def test_scrape_run_read_endpoints(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    source = _seed_source(api_db_session, profiles[0].id)

    run = ScrapeRun(
        source_id=source.id,
        status="completed",
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        duration_ms=75,
        records_seen=10,
        records_inserted=5,
        records_updated=2,
        duplicates=2,
        failures=1,
    )
    api_db_session.add(run)
    api_db_session.commit()
    api_db_session.refresh(run)

    list_response = api_client.get("/scrape-runs")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = api_client.get(f"/scrape-runs/{run.id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == run.id


def test_scrape_run_get_404(api_client) -> None:
    response = api_client.get("/scrape-runs/9999")
    assert response.status_code == 404


def test_job_listing_filters(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    source = _seed_source(api_db_session, profiles[0].id)

    listing = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="greenhouse:abc",
        title="Python Engineer",
        company="Example Co",
        location="Remote",
        work_mode="remote",
        employment_type="full-time",
        posted_at=datetime.now(timezone.utc),
        apply_url="https://jobs.example.com/python-engineer",
        description_snippet="Build backend services",
        tags=["backend"],
        skills=["Python"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    api_db_session.add(listing)
    api_db_session.commit()

    response = api_client.get("/job-listings", params={"title_query": "Python", "limit": 10, "offset": 0})

    assert response.status_code == 200
    payload = response.json()
    assert payload["limit"] == 10
    assert payload["offset"] == 0
    assert len(payload["items"]) == 1
    assert payload["items"][0]["title"] == "Python Engineer"
    assert payload["items"][0]["bookmark_status"] == "new"


def test_bookmark_upsert(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    source = _seed_source(api_db_session, profiles[0].id)

    listing = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="greenhouse:def",
        title="Vue Developer",
        company="Example Co",
        location="Manila",
        work_mode="hybrid",
        employment_type="full-time",
        posted_at=datetime.now(timezone.utc),
        apply_url="https://jobs.example.com/vue",
        description_snippet="Build UI",
        tags=["frontend"],
        skills=["Vue"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    api_db_session.add(listing)
    api_db_session.commit()
    api_db_session.refresh(listing)

    response = api_client.put(
        f"/job-listings/{listing.id}/bookmark",
        json={"status": "interested", "notes": "High priority"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["job_id"] == listing.id
    assert payload["status"] == "interested"

    listing_response = api_client.get("/job-listings", params={"limit": 10, "offset": 0})
    assert listing_response.status_code == 200
    listing_payload = listing_response.json()
    assert listing_payload["items"][0]["bookmark_status"] == "interested"


def test_job_listing_bookmark_status_and_export_stay_consistent(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    source = _seed_source(api_db_session, profiles[0].id)

    listing = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="consistency-1",
        title="Backend Engineer",
        company="Acme",
        location="Remote",
        work_mode="remote",
        employment_type="full-time",
        posted_at=datetime.now(timezone.utc),
        apply_url="https://jobs.example.com/backend-1",
        description_snippet="Build APIs",
        tags=["backend"],
        skills=["Python"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    api_db_session.add(listing)
    api_db_session.commit()
    api_db_session.refresh(listing)

    bookmark = JobBookmark(
        job_id=listing.id,
        status="applied",
        notes=None,
        updated_at=datetime.now(timezone.utc),
    )
    api_db_session.add(bookmark)
    api_db_session.commit()

    listing_response = api_client.get("/job-listings", params={"limit": 10, "offset": 0})
    assert listing_response.status_code == 200
    listing_payload = listing_response.json()
    assert listing_payload["items"][0]["bookmark_status"] == "applied"

    export_response = api_client.post(
        "/exports",
        json={"format": "csv", "filters": {"limit": 100, "offset": 0}},
    )
    assert export_response.status_code == 200

    rows = list(csv.DictReader(io.StringIO(export_response.text)))
    assert len(rows) == 1
    assert rows[0]["bookmark_status"] == "applied"


def test_bookmark_upsert_404_when_listing_missing(api_client) -> None:
    response = api_client.put("/job-listings/9999/bookmark", json={"status": "new", "notes": None})
    assert response.status_code == 404


def test_post_scrape_runs_with_selected_sources(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = JobSource(
        name="GH Source",
        base_url="https://boards.greenhouse.io/example",
        profile_id=greenhouse.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1"}, {"id": "job-2"}]},
    )
    api_db_session.add(source)
    api_db_session.commit()
    api_db_session.refresh(source)

    response = api_client.post("/scrape-runs", json={"source_ids": [source.id]})

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["metrics"]["records_seen"] == 2
    assert payload["metrics"]["records_inserted"] == 2
    assert payload["metrics"]["records_updated"] == 0
    assert payload["metrics"]["duplicates"] == 0
    assert payload["metrics"]["failures"] == 0
    assert payload["metrics"]["duration_ms"] >= 0

    run_id = payload["run_id"]
    raw_rows = list(api_db_session.scalars(select(RawJob).where(RawJob.scrape_run_id == run_id)).all())
    assert len(raw_rows) == 2
    listing_rows = list(api_db_session.scalars(select(JobListing)).all())
    assert len(listing_rows) == 2


def test_post_scrape_runs_without_source_ids_uses_enabled_sources(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = JobSource(
        name="GH Source Enabled",
        base_url="https://boards.greenhouse.io/example",
        profile_id=greenhouse.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1"}]},
    )
    api_db_session.add(source)
    api_db_session.commit()

    response = api_client.post("/scrape-runs", json={})
    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["metrics"]["records_seen"] == 1
    assert payload["metrics"]["records_inserted"] == 1


def test_repeated_scrape_does_not_create_duplicate_job_listing(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = JobSource(
        name="GH Source Repeated",
        base_url="https://boards.greenhouse.io/example",
        profile_id=greenhouse.id,
        enabled=True,
        config={"fixtures": [{"id": "job-1", "title": "Python Engineer"}]},
    )
    api_db_session.add(source)
    api_db_session.commit()
    api_db_session.refresh(source)

    first = api_client.post("/scrape-runs", json={"source_ids": [source.id]})
    second = api_client.post("/scrape-runs", json={"source_ids": [source.id]})

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["metrics"]["records_inserted"] == 1
    assert second.json()["metrics"]["records_inserted"] == 0
    assert second.json()["metrics"]["duplicates"] == 1

    listings = list(api_db_session.scalars(select(JobListing)).all())
    raw_jobs = list(api_db_session.scalars(select(RawJob)).all())
    assert len(listings) == 1
    assert len(raw_jobs) == 2


def test_exports_csv_download_response(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = _seed_source(api_db_session, greenhouse.id)
    listing = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="exp-1",
        title="Python Engineer",
        company="Acme",
        location="Remote",
        work_mode="remote",
        employment_type="full-time",
        posted_at=datetime.now(timezone.utc),
        apply_url="https://jobs.example.com/1",
        description_snippet="Build APIs",
        tags=["backend"],
        skills=["Python"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    api_db_session.add(listing)
    api_db_session.commit()

    response = api_client.post(
        "/exports",
        json={"format": "csv", "filters": {"title_query": "Python", "limit": 100, "offset": 0}},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment; filename=\"job-export-" in response.headers["content-disposition"]
    assert "title,company,location" in response.text
    assert "Python Engineer" in response.text


def test_exports_xlsx_download_response(api_client, api_db_session: Session) -> None:
    profiles = _seed_profiles(api_db_session)
    greenhouse = next(profile for profile in profiles if profile.code == "greenhouse")
    source = _seed_source(api_db_session, greenhouse.id)
    listing = JobListing(
        source_id=source.id,
        raw_job_id=None,
        canonical_key="exp-2",
        title="Vue Developer",
        company="Acme",
        location="Manila",
        work_mode="hybrid",
        employment_type="full-time",
        posted_at=datetime.now(timezone.utc),
        apply_url="https://jobs.example.com/2",
        description_snippet="Build UI",
        tags=["frontend"],
        skills=["Vue"],
        first_seen_at=datetime.now(timezone.utc),
        last_seen_at=datetime.now(timezone.utc),
        is_active=True,
    )
    api_db_session.add(listing)
    api_db_session.commit()

    response = api_client.post("/exports", json={"format": "xlsx", "filters": {"limit": 100, "offset": 0}})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "attachment; filename=\"job-export-" in response.headers["content-disposition"]
    assert len(response.content) > 100


def test_exports_empty_csv_includes_headers(api_client) -> None:
    response = api_client.post("/exports", json={"format": "csv", "filters": {}})
    assert response.status_code == 200
    assert response.text.startswith("title,company,location")


def test_exports_invalid_format_validation(api_client) -> None:
    response = api_client.post("/exports", json={"format": "pdf", "filters": {}})
    assert response.status_code == 422
