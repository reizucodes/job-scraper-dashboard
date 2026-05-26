from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_scrape_run_service
from app.schemas.scrape_run import (
    ScrapeRunMetricsResponse,
    ScrapeRunResponse,
    ScrapeRunTriggerRequest,
    ScrapeRunTriggerResponse,
)
from app.services.scrape_run_service import ScrapeRunService

router = APIRouter(prefix="/scrape-runs", tags=["scrape-runs"])


@router.post("", response_model=ScrapeRunTriggerResponse, status_code=status.HTTP_201_CREATED)
def trigger_scrape_run(
    payload: ScrapeRunTriggerRequest,
    service: ScrapeRunService = Depends(get_scrape_run_service),
) -> ScrapeRunTriggerResponse:
    result = service.trigger_run(source_ids=payload.source_ids)
    run = result.run
    return ScrapeRunTriggerResponse(
        run_id=run.id,
        status=run.status,
        metrics=ScrapeRunMetricsResponse(
            records_seen=run.records_seen,
            records_inserted=run.records_inserted,
            records_updated=run.records_updated,
            duplicates=run.duplicates,
            failures=run.failures,
            duration_ms=run.duration_ms or 0,
        ),
    )


@router.get("", response_model=list[ScrapeRunResponse])
def list_scrape_runs(
    limit: int = Query(default=50, ge=1, le=200),
    service: ScrapeRunService = Depends(get_scrape_run_service),
) -> list[ScrapeRunResponse]:
    runs = service.list_runs(limit=limit)
    return [ScrapeRunResponse.model_validate(run) for run in runs]


@router.get("/{run_id}", response_model=ScrapeRunResponse)
def get_scrape_run(run_id: int, service: ScrapeRunService = Depends(get_scrape_run_service)) -> ScrapeRunResponse:
    run = service.get_run(run_id)
    return ScrapeRunResponse.model_validate(run)
