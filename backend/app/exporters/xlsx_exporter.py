from __future__ import annotations

import io

from openpyxl import Workbook

from app.exporters.contracts import EXPORT_COLUMNS, ExportArtifact


class XlsxExporter:
    format_name = "xlsx"

    def export(self, rows: list[dict[str, str]], columns: tuple[str, ...] = EXPORT_COLUMNS) -> ExportArtifact:
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "jobs"

        sheet.append(list(columns))
        for row in rows:
            sheet.append([row.get(column, "") for column in columns])

        output = io.BytesIO()
        workbook.save(output)

        return ExportArtifact(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            file_extension="xlsx",
        )
