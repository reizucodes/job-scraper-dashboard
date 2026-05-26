from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.db.models.job_source import JobSource
from app.scrapers.contracts import ScrapedRecord


@dataclass(slots=True)
class NormalizedJobData:
    title: str
    company: str
    location: str | None
    work_mode: str | None
    employment_type: str | None
    posted_at: datetime | None
    apply_url: str
    description_snippet: str | None
    tags: list[str]
    skills: list[str]


class NormalizationService:
    def normalize(self, profile_code: str, source: JobSource, record: ScrapedRecord) -> NormalizedJobData:
        payload = record.raw_payload

        title = self._pick_str(payload, self._title_keys(profile_code)) or "Unknown Title"
        company = self._pick_str(payload, self._company_keys(profile_code)) or "Unknown Company"
        location = self._pick_location(payload) or None
        work_mode = self._pick_work_mode(payload)
        employment_type = self._pick_str(payload, ["employment_type", "commitment", "type"]) or None
        posted_at = self._parse_datetime(self._pick_str(payload, ["posted_at", "created_at", "updated_at", "date_posted"]))
        apply_url = self._pick_str(payload, ["apply_url", "absolute_url", "url", "hosted_url"]) or source.base_url
        description_snippet = self._pick_str(payload, ["description_snippet", "description", "content"]) or None

        tags = self._normalize_string_list(payload.get("tags"))
        skills = self._normalize_string_list(payload.get("skills"))

        return NormalizedJobData(
            title=title,
            company=company,
            location=location,
            work_mode=work_mode,
            employment_type=employment_type,
            posted_at=posted_at,
            apply_url=apply_url,
            description_snippet=description_snippet,
            tags=tags,
            skills=skills,
        )

    @staticmethod
    def _title_keys(profile_code: str) -> list[str]:
        if profile_code == "lever":
            return ["text", "title", "name"]
        if profile_code == "greenhouse":
            return ["title", "text", "name"]
        return ["title", "name", "text"]

    @staticmethod
    def _company_keys(profile_code: str) -> list[str]:
        if profile_code == "custom-html":
            return ["company", "company_name", "org"]
        return ["company", "company_name", "organization", "org"]

    @staticmethod
    def _pick_str(payload: dict[str, object], keys: list[str]) -> str | None:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, str):
                normalized = value.strip()
                if normalized:
                    return normalized
        return None

    @staticmethod
    def _normalize_mode(value: str | None) -> str | None:
        if value is None:
            return None
        lowered = value.strip().lower()
        if lowered in {"remote", "hybrid", "onsite", "on-site"}:
            return "onsite" if lowered == "on-site" else lowered
        return lowered or None

    @staticmethod
    def _normalize_string_list(value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        result: list[str] = []
        for item in value:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    result.append(cleaned)
        return result

    @classmethod
    def _pick_work_mode(cls, payload: dict[str, object]) -> str | None:
        direct = cls._pick_str(payload, ["work_mode", "mode", "workplace"])
        if direct is not None:
            normalized = cls._normalize_mode(direct)
            if normalized is not None:
                return normalized

        metadata = payload.get("metadata")
        if isinstance(metadata, list):
            for item in metadata:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                value = item.get("value")
                if not isinstance(name, str) or not isinstance(value, str):
                    continue
                normalized_name = name.strip().lower()
                if normalized_name in {"location type", "work location", "work mode", "workplace type"}:
                    normalized_value = cls._normalize_mode(value)
                    if normalized_value is not None:
                        return normalized_value
        return None

    @classmethod
    def _pick_location(cls, payload: dict[str, object]) -> str | None:
        direct = cls._pick_str(payload, ["location", "job_location", "city"])
        if direct is not None:
            return direct

        location_obj = payload.get("location")
        if isinstance(location_obj, dict):
            name_value = location_obj.get("name")
            if isinstance(name_value, str):
                normalized = name_value.strip()
                if normalized:
                    return normalized

        categories = payload.get("categories")
        if isinstance(categories, dict):
            location_value = categories.get("location")
            if isinstance(location_value, str):
                normalized = location_value.strip()
                if normalized:
                    return normalized
        return None

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if value is None:
            return None
        text = value.strip()
        if not text:
            return None

        normalized = text.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            return None

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
