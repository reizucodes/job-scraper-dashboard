from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ExportFilters(BaseModel):
    source_id: int | None = None
    is_active: bool | None = None
    work_mode: str | None = None
    location: str | None = None
    title_query: str | None = None
    posted_from: datetime | None = None
    posted_to: datetime | None = None
    limit: int = Field(default=1000, ge=1, le=10000)
    offset: int = Field(default=0, ge=0)


class ExportRequest(BaseModel):
    format: Literal["csv", "xlsx"]
    filters: ExportFilters = Field(default_factory=ExportFilters)
