from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RawJobCreate(BaseModel):
    source_id: int
    scrape_run_id: int
    external_ref: str | None = Field(default=None, max_length=255)
    source_snapshot: str | None = None
    raw_payload: dict[str, Any]
    payload_hash: str = Field(min_length=1, max_length=128)
    scraped_at: datetime


class RawJobResponse(BaseModel):
    id: int
    source_id: int
    scrape_run_id: int
    external_ref: str | None
    payload_hash: str
    scraped_at: datetime
