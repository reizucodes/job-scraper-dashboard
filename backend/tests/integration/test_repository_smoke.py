from app.db.seeds import seed_source_profiles
from app.repositories.source_profile_repo import SQLAlchemySourceProfileRepository


def test_seed_and_read_profile_repository(db_session) -> None:
    seed_source_profiles(db_session)
    db_session.commit()

    repo = SQLAlchemySourceProfileRepository(db_session)
    codes = [profile.code for profile in repo.list_all()]

    assert codes == ["custom-html", "greenhouse", "lever"]
