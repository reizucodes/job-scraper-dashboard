from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_job_bookmark_service
from app.schemas.bookmark import JobBookmarkResponse, JobBookmarkUpsert
from app.services.job_bookmark_service import JobBookmarkService

router = APIRouter(prefix="/job-listings", tags=["bookmarks"])


@router.put("/{listing_id}/bookmark", response_model=JobBookmarkResponse)
def upsert_bookmark(
    listing_id: int,
    payload: JobBookmarkUpsert,
    service: JobBookmarkService = Depends(get_job_bookmark_service),
) -> JobBookmarkResponse:
    bookmark = service.upsert(listing_id=listing_id, payload=payload)
    return JobBookmarkResponse.model_validate(bookmark)
