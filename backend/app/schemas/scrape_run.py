from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ScrapeRunCreate(BaseModel):
    source_id: int | None = None
    status: str
    started_at: datetime


class ScrapeRunTriggerRequest(BaseModel):
    source_ids: list[int] | None = Field(default=None)


class ScrapeRunMetricsResponse(BaseModel):
    records_seen: int
    records_inserted: int
    records_updated: int
    duplicates: int
    failures: int
    duration_ms: int


class ScrapeRunTriggerResponse(BaseModel):
    run_id: int
    status: str
    metrics: ScrapeRunMetricsResponse


class ScrapeRunResponse(ORMModel):
    id: int
    source_id: int | None
    status: str
    started_at: datetime
    ended_at: datetime | None
    duration_ms: int | None
    records_seen: int
    records_inserted: int
    records_updated: int
    duplicates: int
    failures: int
    error_summary: str | None
