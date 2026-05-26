# Learning Roadmap (Laravel Developer)

This roadmap is ordered to move from product context to implementation details and then operational usage.

## 1. Overview
Read: `docs/overview.md`

Teaches:
- End-to-end product behavior and system boundaries.

Why it matters:
- Sets mental model before diving into layer details.

Laravel mapping:
- Similar to understanding route groups + service boundaries before editing controllers.

Explore next files:
- `backend/app/main.py`
- `frontend/src/main.ts`

## 2. Backend Architecture
Read: `docs/backend-architecture.md`

Teaches:
- FastAPI layering and DI composition.

Why it matters:
- Most business behavior lives in backend services.

Laravel mapping:
- Controller + Service + Repository + Model mapping table.

Explore next files:
- `backend/app/api/deps.py`
- `backend/app/services/*.py`

## 3. Database and Migrations
Read: `docs/database-and-migrations.md`

Teaches:
- Schema model, relationships, migration + seed behavior.

Why it matters:
- The scrape and export behavior depends on table semantics.

Laravel mapping:
- Eloquent/Migrations/Seeders equivalent patterns.

Explore next files:
- `backend/alembic/versions/20260526_0001_initial_schema.py`
- `backend/app/db/models/*.py`

## 4. Scraping Pipeline
Read: `docs/scraping-pipeline.md`

Teaches:
- Adapter-based ingestion, normalization, dedupe, run metrics.

Why it matters:
- This is the core differentiator of the app.

Laravel mapping:
- Job ingestion service with provider-specific handlers.

Explore next files:
- `backend/app/services/scrape_run_service.py`
- `backend/app/scrapers/profiles/*.py`

## 5. Frontend Architecture
Read: `docs/frontend-architecture.md`

Teaches:
- Vue route/view/store/api separation and UI composition.

Why it matters:
- Clarifies where to make UI vs state vs transport changes.

Laravel mapping:
- SPA module organization similar to Vue/Inertia projects.

Explore next files:
- `frontend/src/views/*.vue`
- `frontend/src/stores/*.ts`

## 6. Data Flow
Read: `docs/data-flow.md`

Teaches:
- Concrete flow for each major use case.

Why it matters:
- Reduces debugging time by showing cross-layer request paths.

Laravel mapping:
- Equivalent to tracing a request from route to DB and back, including frontend call chain.

Explore next files:
- `frontend/src/api/*.ts`
- `backend/app/api/routers/*.py`

## 7. Request Lifecycle
Read: `docs/request-lifecycle.md`

Teaches:
- Detailed sequence diagrams for create source, run scrape, bookmark update, export.

Why it matters:
- Helps reason about side effects, commit points, and failure handling.

Laravel mapping:
- Similar to full controller/service/repo trace docs.

Explore next files:
- `backend/app/services/job_source_service.py`
- `backend/app/services/export_service.py`

## 8. API Reference
Read: `docs/api-reference.md`

Teaches:
- Implemented endpoint contracts, examples, and errors.

Why it matters:
- Required for frontend integration and external tooling.

Laravel mapping:
- Equivalent to API docs generated from controller contracts.

Explore next files:
- `backend/app/schemas/*.py`

## 9. Developer Guide
Read: `docs/developer-guide.md`

Teaches:
- Setup, run, test, build, troubleshooting workflows.

Why it matters:
- Operational baseline for local development and debugging.

Laravel mapping:
- Similar to project README + team runbook.

Explore next files:
- `Makefile`
- `backend/pyproject.toml`
- `frontend/package.json`
