from __future__ import annotations

from app.db.models.source_profile import SourceProfile
from app.repositories.interfaces import SourceProfileRepository


class SourceProfileService:
    def __init__(self, repository: SourceProfileRepository) -> None:
        self._repository = repository

    def list_source_profiles(self, active_only: bool = True) -> list[SourceProfile]:
        if active_only:
            return self._repository.list_active()
        return self._repository.list_all()
