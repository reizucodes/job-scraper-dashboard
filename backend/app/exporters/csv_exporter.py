from __future__ import annotations

import csv
import io

from app.exporters.contracts import EXPORT_COLUMNS, ExportArtifact


class CsvExporter:
    format_name = "csv"

    def export(self, rows: list[dict[str, str]], columns: tuple[str, ...] = EXPORT_COLUMNS) -> ExportArtifact:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})

        return ExportArtifact(
            content=output.getvalue().encode("utf-8"),
            media_type="text/csv; charset=utf-8",
            file_extension="csv",
        )
