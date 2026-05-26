from __future__ import annotations

from typing import Any

from pydantic import AnyUrl, TypeAdapter, ValidationError

from app.services.errors import ValidationServiceError

_URL_ADAPTER = TypeAdapter(AnyUrl)
_LIVE_PROFILES = {"greenhouse", "lever"}
_VALID_MODES = {"fixture", "live"}
_TIMEOUT_MIN = 1
_TIMEOUT_MAX = 30


class JobSourceConfigValidator:
    def validate(self, profile_code: str, config: dict[str, Any]) -> dict[str, Any]:
        errors: list[str] = []
        normalized = dict(config)

        mode_value = normalized.get("mode", "fixture")
        mode = str(mode_value).lower()
        normalized["mode"] = mode
        if mode not in _VALID_MODES:
            errors.append("config.mode must be either 'fixture' or 'live'")

        timeout = normalized.get("timeout_seconds")
        if timeout is not None:
            if not isinstance(timeout, int):
                errors.append("config.timeout_seconds must be an integer between 1 and 30")
            elif timeout < _TIMEOUT_MIN or timeout > _TIMEOUT_MAX:
                errors.append("config.timeout_seconds must be between 1 and 30")

        user_agent = normalized.get("user_agent")
        if user_agent is not None and not isinstance(user_agent, str):
            errors.append("config.user_agent must be a string")

        if mode == "fixture":
            fixtures = normalized.get("fixtures")
            if fixtures is not None:
                if not isinstance(fixtures, list) or not all(isinstance(item, dict) for item in fixtures):
                    errors.append("config.fixtures must be a list of objects when provided")

        if mode == "live" and profile_code in _LIVE_PROFILES:
            jobs_url = normalized.get("jobs_url")
            if not isinstance(jobs_url, str) or not jobs_url.strip():
                errors.append("config.jobs_url is required for live mode")
            else:
                try:
                    _URL_ADAPTER.validate_python(jobs_url)
                except ValidationError:
                    errors.append("config.jobs_url must be a valid URL")

        if errors:
            raise ValidationServiceError("Invalid job source config", errors=errors)
        return normalized
