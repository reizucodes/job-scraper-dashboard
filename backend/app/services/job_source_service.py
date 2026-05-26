from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.job_source import JobSource
from app.repositories.interfaces import JobSourceRepository, SourceProfileRepository
from app.schemas.job_source import JobSourceCreate, JobSourceUpdate
from app.services.errors import NotFoundError
from app.services.job_source_config_validator import JobSourceConfigValidator


class JobSourceService:
    def __init__(
        self,
        session: Session,
        source_repository: JobSourceRepository,
        profile_repository: SourceProfileRepository,
        config_validator: JobSourceConfigValidator | None = None,
    ) -> None:
        self._session = session
        self._source_repository = source_repository
        self._profile_repository = profile_repository
        self._config_validator = config_validator or JobSourceConfigValidator()

    def create(self, payload: JobSourceCreate) -> JobSource:
        profile = self._profile_repository.get(payload.profile_id)
        if profile is None:
            profile_id = payload.profile_id
            raise NotFoundError(f"Source profile {profile_id} not found")
        validated_config = self._config_validator.validate(profile.code, payload.config)

        source = JobSource(
            name=payload.name,
            base_url=str(payload.base_url),
            profile_id=payload.profile_id,
            enabled=payload.enabled,
            config=validated_config,
        )
        created = self._source_repository.create(source)
        self._session.commit()
        self._session.refresh(created)
        return created

    def list_all(self) -> list[JobSource]:
        return self._source_repository.list_all()

    def update(self, source_id: int, payload: JobSourceUpdate) -> JobSource:
        source = self._source_repository.get(source_id)
        if source is None:
            raise NotFoundError(f"Job source {source_id} not found")
        profile = self._profile_repository.get(source.profile_id)
        if profile is None:
            raise NotFoundError(f"Source profile {source.profile_id} not found")

        if payload.name is not None:
            source.name = payload.name
        if payload.base_url is not None:
            source.base_url = str(payload.base_url)
        if payload.enabled is not None:
            source.enabled = payload.enabled
        if payload.config is not None:
            source.config = self._config_validator.validate(profile.code, payload.config)

        updated = self._source_repository.update(source)
        self._session.commit()
        self._session.refresh(updated)
        return updated

    def delete(self, source_id: int) -> None:
        deleted = self._source_repository.delete(source_id)
        if not deleted:
            raise NotFoundError(f"Job source {source_id} not found")
        self._session.commit()
