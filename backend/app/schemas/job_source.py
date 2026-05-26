from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl

from app.schemas.common import TimestampedResponse


class JobSourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_url: HttpUrl
    profile_id: int
    enabled: bool = True
    config: dict[str, Any] = Field(default_factory=dict)


class JobSourceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    base_url: HttpUrl | None = None
    enabled: bool | None = None
    config: dict[str, Any] | None = None


class JobSourceResponse(TimestampedResponse):
    id: int
    name: str
    base_url: str
    profile_id: int
    enabled: bool
    config: dict[str, Any]
