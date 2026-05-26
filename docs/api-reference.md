# API Reference

Base URL (default local): `http://localhost:8000`

Error format (service-level mapped):
- 404/409: `{ "detail": "..." }`
- 422 from `ValidationServiceError`: `{ "detail": "...", "errors": ["..."] }`

## 1) GET `/source-profiles`
Purpose:
- List source profiles.

Query params:
- `active_only` (bool, default `true`)

Response example:
```json
[
  {
    "id": 1,
    "code": "greenhouse",
    "display_name": "Greenhouse",
    "active": true,
    "created_at": "2026-05-26T00:00:00Z",
    "updated_at": "2026-05-26T00:00:00Z"
  }
]
```

## 2) POST `/job-sources`
Purpose:
- Create a job source.

Request example:
```json
{
  "name": "Anthropic GH",
  "base_url": "https://www.anthropic.com/careers",
  "profile_id": 1,
  "enabled": true,
  "config": {
    "mode": "live",
    "jobs_url": "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs",
    "timeout_seconds": 10,
    "user_agent": "job-scraper-dashboard/1.0"
  }
}
```

Validation rules:
- `name`: required, 1..255.
- `base_url`: valid URL.
- `profile_id`: must exist.
- `config.mode`: `fixture|live`.
- `config.timeout_seconds`: int 1..30 when provided.
- `config.user_agent`: string when provided.
- live mode on greenhouse/lever requires valid `config.jobs_url`.
- fixture `config.fixtures` must be list of objects when provided.

Response:
- `201` with created source payload.

Error scenarios:
- `404` profile missing.
- `422` config validation errors.

## 3) GET `/job-sources`
Purpose:
- List all job sources.

Response example:
```json
[
  {
    "id": 1,
    "name": "Anthropic",
    "base_url": "https://www.anthropic.com/careers",
    "profile_id": 1,
    "enabled": true,
    "config": {"mode": "live", "jobs_url": "..."},
    "created_at": "2026-05-26T00:00:00Z",
    "updated_at": "2026-05-26T00:00:00Z"
  }
]
```

## 4) PATCH `/job-sources/{id}`
Purpose:
- Partial update for source fields.

Request example:
```json
{
  "enabled": false
}
```

Or config update:
```json
{
  "config": {
    "mode": "fixture",
    "fixtures": [{"id": "job-1", "title": "Python Engineer"}]
  }
}
```

Response:
- `200` updated source.

Errors:
- `404` source missing.
- `422` invalid config payload.

## 5) DELETE `/job-sources/{id}`
Purpose:
- Delete a source.

Response:
- `204 No Content`

Errors:
- `404` source missing.

## 6) POST `/scrape-runs`
Purpose:
- Trigger synchronous scrape run.

Request example (all enabled sources):
```json
{}
```

Request example (selected sources):
```json
{ "source_ids": [1, 2] }
```

Behavior notes:
- Selected disabled sources are not scraped and are recorded as failures.
- Missing source IDs are recorded as failures.
- Run status is `failed` when any failures occurred.

Response example:
```json
{
  "run_id": 12,
  "status": "failed",
  "metrics": {
    "records_seen": 10,
    "records_inserted": 8,
    "records_updated": 1,
    "duplicates": 1,
    "failures": 2,
    "duration_ms": 1234
  }
}
```

## 7) GET `/scrape-runs`
Purpose:
- List recent runs.

Query params:
- `limit` (1..200, default 50)

Response:
- Array of run objects with status, metrics, timing, and `error_summary`.

## 8) GET `/scrape-runs/{id}`
Purpose:
- Get run details.

Response:
- Run object.

Errors:
- `404` run not found.

## 9) GET `/job-listings`
Purpose:
- List normalized job listings.

Query params:
- `source_id`
- `is_active`
- `work_mode`
- `location`
- `title_query`
- `posted_from`
- `posted_to`
- `limit` (1..200, default 50)
- `offset` (>=0)

Response example:
```json
{
  "items": [
    {
      "id": 22,
      "source_id": 1,
      "raw_job_id": 90,
      "canonical_key": "src:1:ext:...",
      "title": "Python Engineer",
      "company": "Acme",
      "location": "Remote",
      "work_mode": "remote",
      "posted_at": "2026-01-01T00:00:00Z",
      "apply_url": "https://jobs.example.com/1",
      "description_snippet": "Build APIs",
      "tags": ["backend"],
      "skills": ["Python"],
      "first_seen_at": "2026-01-01T00:00:00Z",
      "last_seen_at": "2026-01-05T00:00:00Z",
      "is_active": true,
      "bookmark_status": "new"
    }
  ],
  "limit": 50,
  "offset": 0
}
```

Bookmark status behavior:
- Hydrated from persisted `job_bookmarks`.
- Defaults to `new` when no bookmark row exists.

## 10) PUT `/job-listings/{id}/bookmark`
Purpose:
- Upsert bookmark status/notes for a listing.

Request example:
```json
{
  "status": "applied",
  "notes": "Submitted via careers page"
}
```

Validation:
- `status`: one of `new|interested|applied|rejected`
- `notes`: optional, max length 5000

Response example:
```json
{
  "id": 7,
  "job_id": 22,
  "status": "applied",
  "notes": "Submitted via careers page",
  "updated_at": "2026-05-26T12:00:00Z"
}
```

Errors:
- `404` listing not found.

## 11) POST `/exports`
Purpose:
- Export filtered listings as CSV or XLSX.

Request example:
```json
{
  "format": "csv",
  "filters": {
    "title_query": "python",
    "limit": 1000,
    "offset": 0
  }
}
```

Validation:
- `format`: `csv|xlsx`
- `filters.limit`: 1..10000
- `filters.offset`: >=0

Response:
- Binary file with `Content-Disposition` filename.
- CSV media type: `text/csv; charset=utf-8`
- XLSX media type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

Exported columns include:
- `title, company, location, work_mode, employment_type, posted_at, apply_url, description_snippet, tags, skills, first_seen_at, last_seen_at, source_id, bookmark_status`
