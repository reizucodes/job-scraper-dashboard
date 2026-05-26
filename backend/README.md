# Backend (FastAPI)

## Local setup
1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies: `pip install -e '.[dev]'`.
3. Apply migrations: `alembic upgrade head`.

## Run
- API server: `uvicorn app.main:app --reload --port 8000`
- Tests: `pytest`

## Notes
- SQLite is used for MVP (`JSD_DATABASE_URL` override supported).
- Source profiles seeded via initial Alembic migration:
  - `greenhouse`
  - `lever`
  - `custom-html`

## Scraper config modes
`JobSource.config` supports `mode: "fixture" | "live"` for provider adapters.

Fixture mode (deterministic local/test behavior):

```json
{
  "mode": "fixture"
}
```

Greenhouse live mode:

```json
{
  "mode": "live",
  "jobs_url": "https://boards-api.greenhouse.io/v1/boards/<board_token>/jobs",
  "user_agent": "job-scraper-dashboard/1.0",
  "timeout_seconds": 10
}
```

Lever live mode:

```json
{
  "mode": "live",
  "jobs_url": "https://api.lever.co/v0/postings/<company>?mode=json",
  "user_agent": "job-scraper-dashboard/1.0",
  "timeout_seconds": 10
}
```

Notes:
- `jobs_url` is required for `mode: "live"`.
- `timeout_seconds` defaults to `10` if omitted.
- `timeout_seconds` must be an integer in range `1..30`.
- `user_agent` defaults to `job-scraper-dashboard/1.0` if omitted.
- `mode` defaults to `fixture` when omitted.
- `fixtures` is optional in fixture mode, but must be a list of objects when provided.
