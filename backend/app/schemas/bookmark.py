from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.db.models.enums import BookmarkStatus
from app.schemas.common import ORMModel


class JobBookmarkUpsert(BaseModel):
    status: BookmarkStatus
    notes: str | None = Field(default=None, max_length=5000)


class JobBookmarkResponse(ORMModel):
    id: int
    job_id: int
    status: BookmarkStatus
    notes: str | None
    updated_at: datetime
