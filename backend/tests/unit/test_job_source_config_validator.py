from __future__ import annotations

import pytest

from app.services.errors import ValidationServiceError
from app.services.job_source_config_validator import JobSourceConfigValidator


def test_fixture_mode_valid_with_fixtures() -> None:
    validator = JobSourceConfigValidator()
    config = validator.validate("greenhouse", {"mode": "fixture", "fixtures": [{"id": "1"}]})
    assert config["mode"] == "fixture"


def test_mode_defaults_to_fixture() -> None:
    validator = JobSourceConfigValidator()
    config = validator.validate("lever", {})
    assert config["mode"] == "fixture"


def test_invalid_mode_raises_validation_error() -> None:
    validator = JobSourceConfigValidator()
    with pytest.raises(ValidationServiceError):
        validator.validate("greenhouse", {"mode": "unknown"})


def test_live_mode_requires_jobs_url_for_greenhouse() -> None:
    validator = JobSourceConfigValidator()
    with pytest.raises(ValidationServiceError):
        validator.validate("greenhouse", {"mode": "live"})


def test_live_mode_rejects_invalid_jobs_url() -> None:
    validator = JobSourceConfigValidator()
    with pytest.raises(ValidationServiceError):
        validator.validate("lever", {"mode": "live", "jobs_url": "not-a-url"})


def test_rejects_timeout_out_of_range() -> None:
    validator = JobSourceConfigValidator()
    with pytest.raises(ValidationServiceError):
        validator.validate("greenhouse", {"mode": "fixture", "timeout_seconds": 99})
