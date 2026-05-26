from __future__ import annotations

from sqlalchemy import select

from app.db.models.job_source import JobSource
from app.db.seeds import seed_job_sources, seed_source_profiles


def test_seed_job_sources_inserts_default_sources(db_session) -> None:
    seed_source_profiles(db_session)
    seed_job_sources(db_session)
    db_session.commit()

    sources = list(db_session.scalars(select(JobSource).order_by(JobSource.id.asc())).all())

    assert [source.name for source in sources] == ["Anthropic", "Stripe"]
    assert sources[0].config["mode"] == "live"
    assert sources[0].config["jobs_url"] == "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs"


def test_seed_job_sources_is_idempotent(db_session) -> None:
    seed_source_profiles(db_session)
    seed_job_sources(db_session)
    seed_job_sources(db_session)
    db_session.commit()

    count = len(list(db_session.scalars(select(JobSource)).all()))
    assert count == 2
