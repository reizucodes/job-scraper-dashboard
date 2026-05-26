from __future__ import annotations

import csv
import io

from app.exporters import CsvExporter


def test_csv_exporter_writes_header_and_rows() -> None:
    exporter = CsvExporter()
    rows = [
        {
            "title": "Python Engineer",
            "company": "Acme",
            "location": "Remote",
            "work_mode": "remote",
            "employment_type": "full-time",
            "posted_at": "2026-01-01T00:00:00+00:00",
            "apply_url": "https://jobs.example.com/1",
            "description_snippet": "Build APIs",
            "tags": "backend",
            "skills": "Python",
            "first_seen_at": "2026-01-01T00:00:00+00:00",
            "last_seen_at": "2026-01-01T00:00:00+00:00",
            "source_id": "1",
            "bookmark_status": "interested",
        }
    ]

    artifact = exporter.export(rows=rows)

    assert artifact.file_extension == "csv"
    assert artifact.media_type.startswith("text/csv")
    reader = csv.reader(io.StringIO(artifact.content.decode("utf-8")))
    all_rows = list(reader)
    assert all_rows[0][0] == "title"
    assert all_rows[1][0] == "Python Engineer"


def test_csv_exporter_empty_rows_still_has_headers() -> None:
    exporter = CsvExporter()
    artifact = exporter.export(rows=[])

    text = artifact.content.decode("utf-8")
    assert text.startswith("title,company,location")
