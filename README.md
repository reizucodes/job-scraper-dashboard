# job-scraper-dashboard

Job listing scraper dashboard with FastAPI backend and Vue 3 + TypeScript frontend.

## Prerequisites
- Python 3.11+
- Node.js 18+

## Quick start (fresh clone)
1. Install everything and run migrations:
   - `make setup`
2. Start backend (Terminal 1):
   - `make backend-dev`
3. Start frontend (Terminal 2):
   - `make frontend-dev`

Frontend defaults to backend URL `http://localhost:8000`.

## Core developer commands
- Backend tests: `make test-backend`
- Frontend tests: `make test-frontend`
- Frontend typecheck/build: `make build-frontend`

## Manual setup (without Makefile)
### Backend
1. `cd backend`
2. `python3 -m venv .venv`
3. `. .venv/bin/activate`
4. `pip install -e '.[dev]'`
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Core flow
1. Add a source in **Sources**.
2. Trigger scrape in **Runs**.
3. Inspect listings in **Jobs**.
4. Update bookmark status and export CSV/XLSX.
