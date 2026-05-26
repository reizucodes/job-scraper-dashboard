from __future__ import annotations

import pytest

from app.scrapers.profiles import CustomHtmlScraperAdapter, GreenhouseScraperAdapter, LeverScraperAdapter
from app.scrapers.registry import ScraperRegistry


def test_registry_resolves_registered_adapters() -> None:
    registry = ScraperRegistry(
        adapters=[
            GreenhouseScraperAdapter(),
            LeverScraperAdapter(),
            CustomHtmlScraperAdapter(),
        ]
    )

    assert registry.has("greenhouse") is True
    assert registry.has("lever") is True
    assert registry.has("custom-html") is True
    assert registry.get("greenhouse").profile_code == "greenhouse"


def test_registry_raises_for_missing_adapter() -> None:
    registry = ScraperRegistry(adapters=[GreenhouseScraperAdapter()])

    with pytest.raises(KeyError):
        registry.get("workday")
