# Project Intelligence Report

## Metadata
- Generated date: 2026-05-26
- Repository name: job-scraper-dashboard
- Primary stack: FastAPI + SQLAlchemy + Alembic (backend), Vue 3 + TypeScript + Pinia + Tailwind (frontend)
- Confidence level: High
- Files inspected summary: root docs, backend app/repositories/services/schemas/migrations/tests, frontend api/stores/views/components/tests, workflow/policy files

## Executive Summary
Repository now contains a working MVP for job-source management, synchronous scrape orchestration, raw + normalized persistence, bookmarking, filtering, and CSV/XLSX exports with passing backend/frontend test suites.

## Stack and Runtime
- Backend: Python/FastAPI (`backend/app/main.py`, `backend/pyproject.toml`)
- Persistence: SQLite with Alembic migrations (`backend/alembic/versions/20260526_0001_initial_schema.py`)
- Frontend: Vue 3 + TS + Vite + Pinia (`frontend/package.json`, `frontend/src/main.ts`)
- Styling: Tailwind CSS (`frontend/tailwind.config.js`, `frontend/src/styles.css`)

## Repository Structure
- Backend application code under `backend/app/` separated by `api`, `services`, `repositories`, `db`, `scrapers`, `exporters`.
- Frontend application code under `frontend/src/` separated by `api`, `stores`, `views`, `components`.
- AI governance/workflows under `.ai/`.

## Architecture Overview
- Service-oriented monolith backend with thin routers and repository-backed services (`backend/app/api/routers/*.py`, `backend/app/services/*.py`).
- Scrape pipeline: source -> adapter -> raw record persistence -> normalization/dedupe -> listing upsert (`backend/app/services/scrape_run_service.py`).
- Frontend uses centralized API modules and Pinia stores; views compose state/actions (`frontend/src/api/*.ts`, `frontend/src/stores/*.ts`, `frontend/src/views/*.vue`).

## Domain Model / Business Concepts
- SourceProfile, JobSource, ScrapeRun, RawJob, JobListing, JobBookmark (`backend/app/db/models/*.py`).
- Export concept with format + filters (`backend/app/schemas/export.py`).

## Feature Inventory
- Source profile listing and source CRUD.
- Scrape run trigger + metrics + history.
- Raw persistence + normalized listing creation/update/duplicate handling.
- Job listing filtering + bookmark update.
- CSV/XLSX export over filtered listings.

## Data Persistence
- SQLAlchemy models with indexed fields for common queries (`backend/app/db/models/job_listing.py`, `backend/app/db/models/scrape_run.py`).
- Alembic initial migration seeds profile codes (`backend/alembic/versions/20260526_0001_initial_schema.py`).

## API / Interface Conventions
- JSON request/response via Pydantic schemas (`backend/app/schemas/*.py`).
- Error mapping for service errors to HTTP status (`backend/app/api/errors.py`).
- Export endpoint returns binary response with content disposition (`backend/app/api/routers/exports.py`).

## Authentication and Authorization
- Unconfirmed: no authn/authz layer present in current MVP routes (by design).

## External Integrations
- No live external scraping/network integrations in tests; adapters are fixture-driven.
- Browser download interaction for frontend export flow.

## Coding Patterns
- Thin controllers, service orchestration, repository interfaces.
- Deterministic normalization and canonical key generation (`backend/app/services/normalization_service.py`, `backend/app/services/dedupe_service.py`).
- Centralized typed frontend API client (`frontend/src/api/client.ts`).

## Testing Strategy
- Backend: pytest unit/integration/API tests (`backend/tests/`).
- Frontend: vitest component/store tests (`frontend/tests/`).
- Build checks include frontend typecheck/build (`frontend/package.json` scripts).

## Build, Tooling, and Deployment
- Backend dependency/tooling configured in `backend/pyproject.toml`.
- Frontend build/test via Vite/Vitest (`frontend/package.json`).
- Tailwind/PostCSS configured for styling build (`frontend/postcss.config.js`).

## Security and Risk Notes
- No secrets embedded in repository-inspected files.
- Public unauthenticated endpoints are acceptable for current local MVP but high risk for public deployment.

## Technical Debt and Fragile Areas
- Frontend tests rely on mocked API modules; no browser E2E coverage yet.
- Bookmark hydration is frontend-local defaulting rather than backend-provided listing field.
- SQLite baseline may constrain concurrent production load (migration path exists).

## AI Implementation Guidance
- Preferred code locations:
  - Backend routes: `backend/app/api/routers/`
  - Backend business logic: `backend/app/services/`
  - Persistence access: `backend/app/repositories/`
  - Frontend views: `frontend/src/views/`
  - Frontend state: `frontend/src/stores/`
- Existing architectural boundaries:
  - Routers should remain thin.
  - Scraper/extractor logic stays in `scrapers` + normalization/dedupe services.
- Existing abstractions to reuse:
  - `ApiClient`, Pinia stores, exporter/scraper registries.
- Repeated implementation patterns:
  - Load/error status in stores.
  - Service error mapping to HTTP errors.
- Patterns to avoid:
  - Embedding network scraping or heavy logic in routes/views.
- Testing expectations:
  - Add pytest + vitest coverage for any behavior changes.
- Risk-sensitive components:
  - Dedupe canonical key logic.
  - Export schema parity.
- Refactor cautions:
  - Preserve API DTO fields used by frontend stores/views.
- Approval gate triggers:
  - Auth introduction, background workers, public deployment hardening, schema-breaking API changes.

## Open Questions
- Should bookmark status be included directly in `GET /job-listings` payload?
- Should scrape orchestration move to async workers post-MVP?
- What max export row size is acceptable before streaming/background processing is required?

## Evidence Index
- `backend/app/main.py`
- `backend/app/api/routers/exports.py`
- `backend/app/api/routers/scrape_runs.py`
- `backend/app/services/scrape_run_service.py`
- `backend/app/services/normalization_service.py`
- `backend/app/services/dedupe_service.py`
- `backend/app/exporters/contracts.py`
- `backend/app/exporters/csv_exporter.py`
- `backend/app/exporters/xlsx_exporter.py`
- `backend/app/db/models/job_listing.py`
- `backend/alembic/versions/20260526_0001_initial_schema.py`
- `backend/tests/`
- `frontend/src/api/client.ts`
- `frontend/src/stores/`
- `frontend/src/views/SourcesView.vue`
- `frontend/src/views/RunsView.vue`
- `frontend/src/views/JobsView.vue`
- `frontend/src/components/shared/`
- `frontend/tests/`
- `frontend/package.json`
- `README.md`
