from __future__ import annotations

from app.schemas.common import TimestampedResponse


class SourceProfileResponse(TimestampedResponse):
    id: int
    code: str
    display_name: str
    active: bool
