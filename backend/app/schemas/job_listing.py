from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from app.db.models.enums import BookmarkStatus
from app.schemas.common import ORMModel


class JobListingCreate(BaseModel):
    source_id: int
    raw_job_id: int | None = None
    canonical_key: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    company: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    work_mode: str | None = Field(default=None, max_length=32)
    employment_type: str | None = Field(default=None, max_length=64)
    posted_at: datetime | None = None
    apply_url: HttpUrl
    description_snippet: str | None = None
    tags: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    first_seen_at: datetime
    last_seen_at: datetime
    is_active: bool = True


class JobListingResponse(ORMModel):
    id: int
    source_id: int
    raw_job_id: int | None
    canonical_key: str
    title: str
    company: str
    location: str | None
    work_mode: str | None
    posted_at: datetime | None
    apply_url: str
    description_snippet: str | None
    tags: list[str]
    skills: list[str]
    first_seen_at: datetime
    last_seen_at: datetime
    is_active: bool
    bookmark_status: BookmarkStatus


class JobListingListResponse(BaseModel):
    items: list[JobListingResponse]
    limit: int
    offset: int
