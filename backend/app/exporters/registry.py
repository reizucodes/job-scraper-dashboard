from __future__ import annotations

from app.exporters.contracts import Exporter


class ExporterRegistry:
    def __init__(self, exporters: list[Exporter]) -> None:
        self._exporters = {exporter.format_name: exporter for exporter in exporters}

    def resolve(self, format_name: str) -> Exporter:
        exporter = self._exporters.get(format_name)
        if exporter is None:
            raise KeyError(f"Unsupported export format '{format_name}'")
        return exporter
