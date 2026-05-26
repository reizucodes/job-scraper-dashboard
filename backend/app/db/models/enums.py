from __future__ import annotations

from enum import StrEnum


class SourceProfileCode(StrEnum):
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    CUSTOM_HTML = "custom-html"
    WORKDAY = "workday"
    ASHBY = "ashby"


class ScrapeRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkMode(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


class BookmarkStatus(StrEnum):
    NEW = "new"
    INTERESTED = "interested"
    APPLIED = "applied"
    REJECTED = "rejected"
