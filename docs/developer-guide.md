# Developer Guide

## Prerequisites
- Python 3.11+
- Node.js 18+

## Setup
### Recommended (`Makefile`)
```bash
make setup
```

This runs:
- backend venv + install + `alembic upgrade head`
- frontend `npm install`

### Manual Backend Setup
```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
```

### Manual Frontend Setup
```bash
cd frontend
npm install
```

## Local Development
### Start Backend
```bash
make backend-dev
# or
cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000
```

### Start Frontend
```bash
make frontend-dev
# or
cd frontend && npm run dev
```

## Migrations
Apply migrations:
```bash
cd backend && . .venv/bin/activate && alembic upgrade head
```

Migration file present:
- `backend/alembic/versions/20260526_0001_initial_schema.py`

## Seeds
Startup seeds run in app lifespan:
- `seed_source_profiles`
- `seed_job_sources`

Files:
- `backend/app/main.py`
- `backend/app/db/seeds.py`

## Testing
### Backend
```bash
make test-backend
# or
cd backend && . .venv/bin/activate && pytest
```

### Frontend
```bash
make test-frontend
# or
cd frontend && npm run test
```

### Frontend Typecheck/Build
```bash
make build-frontend
# or
cd frontend && npm run build
```

## Exports
- Triggered from Jobs view via `exports` store.
- Backend endpoint: `POST /exports`.
- Supported formats: CSV, XLSX.

## Scraper Testing
Relevant tests:
- Adapter behavior: `backend/tests/unit/test_live_scraper_adapters.py`
- Orchestration and persistence: `backend/tests/integration/test_scrape_run_service.py`
- Route-level scrape behavior: `backend/tests/api/test_phase3_routes.py`

## Debugging Guide

### Backend request path debugging
1. Router function in `backend/app/api/routers/*`.
2. Dependency wiring in `backend/app/api/deps.py`.
3. Service logic in `backend/app/services/*`.
4. Repository SQL in `backend/app/repositories/*`.

### Frontend request path debugging
1. View event handler (`frontend/src/views/*`).
2. Store action (`frontend/src/stores/*`).
3. API module (`frontend/src/api/*`).
4. `ApiClient` request/response handling.

## Common Issues

### CORS Issues
Symptoms:
- Browser rejects calls from frontend dev server.

Current allowed origins:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

File:
- `backend/app/main.py`

### Migration Issues
Symptoms:
- Missing table errors at runtime.

Checks:
1. Activate backend venv.
2. Run `alembic upgrade head`.
3. Ensure DB URL points to intended file (`JSD_DATABASE_URL` override).

### Frontend API Issues
Symptoms:
- `ApiError` with status and raw response text.

Checks:
1. Verify `VITE_API_BASE_URL`.
2. Check backend server is running on expected host/port.
3. Inspect network payloads for 422 schema/config validation errors.

## Useful Maintenance Commands
```bash
make fresh-install
make clean-backend
make clean-frontend
make reset-db
```
