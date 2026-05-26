from __future__ import annotations

from app.scrapers.contracts import ScraperAdapter


class ScraperRegistry:
    def __init__(self, adapters: list[ScraperAdapter]) -> None:
        self._adapters = {adapter.profile_code: adapter for adapter in adapters}

    def get(self, profile_code: str) -> ScraperAdapter:
        adapter = self._adapters.get(profile_code)
        if adapter is None:
            raise KeyError(f"No scraper adapter registered for profile '{profile_code}'")
        return adapter

    def has(self, profile_code: str) -> bool:
        return profile_code in self._adapters
