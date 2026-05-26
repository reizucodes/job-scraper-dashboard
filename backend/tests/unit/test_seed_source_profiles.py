from sqlalchemy import select

from app.db.models.source_profile import SourceProfile
from app.db.seeds import seed_source_profiles


def test_seed_source_profiles_inserts_default_set(db_session) -> None:
    seed_source_profiles(db_session)
    db_session.commit()

    profiles = list(db_session.scalars(select(SourceProfile).order_by(SourceProfile.code.asc())).all())

    assert [profile.code for profile in profiles] == ["custom-html", "greenhouse", "lever"]


def test_seed_source_profiles_is_idempotent(db_session) -> None:
    seed_source_profiles(db_session)
    seed_source_profiles(db_session)
    db_session.commit()

    count = len(list(db_session.scalars(select(SourceProfile)).all()))
    assert count == 3
