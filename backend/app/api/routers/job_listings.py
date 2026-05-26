from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_job_listing_service
from app.schemas.job_listing import JobListingListResponse, JobListingResponse
from app.services.job_listing_service import JobListingService

router = APIRouter(prefix="/job-listings", tags=["job-listings"])


@router.get("", response_model=JobListingListResponse)
def list_job_listings(
    source_id: int | None = None,
    is_active: bool | None = None,
    work_mode: str | None = None,
    location: str | None = None,
    title_query: str | None = None,
    posted_from: datetime | None = None,
    posted_to: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: JobListingService = Depends(get_job_listing_service),
) -> JobListingListResponse:
    result = service.list_listings(
        source_id=source_id,
        is_active=is_active,
        work_mode=work_mode,
        location=location,
        title_query=title_query,
        posted_from=posted_from,
        posted_to=posted_to,
        limit=limit,
        offset=offset,
    )
    items: list[JobListingResponse] = []
    for item in result.items:
        payload = {
            "id": item.id,
            "source_id": item.source_id,
            "raw_job_id": item.raw_job_id,
            "canonical_key": item.canonical_key,
            "title": item.title,
            "company": item.company,
            "location": item.location,
            "work_mode": item.work_mode,
            "posted_at": item.posted_at,
            "apply_url": item.apply_url,
            "description_snippet": item.description_snippet,
            "tags": item.tags,
            "skills": item.skills,
            "first_seen_at": item.first_seen_at,
            "last_seen_at": item.last_seen_at,
            "is_active": item.is_active,
            "bookmark_status": result.bookmark_status_by_listing_id.get(item.id, "new"),
        }
        items.append(JobListingResponse.model_validate(payload))
    return JobListingListResponse(
        items=items,
        limit=result.limit,
        offset=result.offset,
    )
