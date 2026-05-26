from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_job_source_service
from app.schemas.job_source import JobSourceCreate, JobSourceResponse, JobSourceUpdate
from app.services.job_source_service import JobSourceService

router = APIRouter(prefix="/job-sources", tags=["job-sources"])


@router.post("", response_model=JobSourceResponse, status_code=status.HTTP_201_CREATED)
def create_job_source(
    payload: JobSourceCreate,
    service: JobSourceService = Depends(get_job_source_service),
) -> JobSourceResponse:
    source = service.create(payload)
    return JobSourceResponse.model_validate(source)


@router.get("", response_model=list[JobSourceResponse])
def list_job_sources(service: JobSourceService = Depends(get_job_source_service)) -> list[JobSourceResponse]:
    sources = service.list_all()
    return [JobSourceResponse.model_validate(source) for source in sources]


@router.patch("/{source_id}", response_model=JobSourceResponse)
def update_job_source(
    source_id: int,
    payload: JobSourceUpdate,
    service: JobSourceService = Depends(get_job_source_service),
) -> JobSourceResponse:
    source = service.update(source_id, payload)
    return JobSourceResponse.model_validate(source)


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_source(source_id: int, service: JobSourceService = Depends(get_job_source_service)) -> Response:
    service.delete(source_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
