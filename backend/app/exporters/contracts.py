from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


EXPORT_COLUMNS: tuple[str, ...] = (
    "title",
    "company",
    "location",
    "work_mode",
    "employment_type",
    "posted_at",
    "apply_url",
    "description_snippet",
    "tags",
    "skills",
    "first_seen_at",
    "last_seen_at",
    "source_id",
    "bookmark_status",
)


@dataclass(slots=True)
class ExportArtifact:
    content: bytes
    media_type: str
    file_extension: str


class Exporter(Protocol):
    format_name: str

    def export(self, rows: list[dict[str, str]], columns: tuple[str, ...] = EXPORT_COLUMNS) -> ExportArtifact: ...
