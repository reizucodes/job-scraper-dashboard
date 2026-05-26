from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_source_profile_service
from app.schemas.source_profile import SourceProfileResponse
from app.services.source_profile_service import SourceProfileService

router = APIRouter(prefix="/source-profiles", tags=["source-profiles"])


@router.get("", response_model=list[SourceProfileResponse])
def list_source_profiles(
    active_only: bool = True,
    service: SourceProfileService = Depends(get_source_profile_service),
) -> list[SourceProfileResponse]:
    profiles = service.list_source_profiles(active_only=active_only)
    return [SourceProfileResponse.model_validate(profile) for profile in profiles]
