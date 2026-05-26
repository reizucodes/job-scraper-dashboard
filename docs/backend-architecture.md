# Backend Architecture

## Purpose
This backend is a layered FastAPI application with explicit boundaries between transport, orchestration, persistence, and integration logic.

## Laravel Mapping Table
| Laravel | FastAPI Project |
|---|---|
| `routes/api.php` + Controller methods | `backend/app/api/routers/*.py` |
| Form Request validation | Pydantic request schemas in `backend/app/schemas/*.py` |
| API Resource / Transformer | Pydantic response schemas in `backend/app/schemas/*.py` |
| Service class | `backend/app/services/*.py` |
| Repository class | `backend/app/repositories/*.py` |
| Eloquent Model | SQLAlchemy model in `backend/app/db/models/*.py` |
| Migration | Alembic migration in `backend/alembic/versions/*.py` |
| Container resolution | FastAPI dependency injection in `backend/app/api/deps.py` |
| Exception handler | `backend/app/api/errors.py` |

## Folder-Level Architecture

### `backend/app/main.py`
File: `backend/app/main.py`

Purpose:
- FastAPI app bootstrap.
- CORS setup.
- Router registration.
- Exception handler registration.
- Startup lifespan seed execution.

Called By:
- Uvicorn (`uvicorn app.main:app ...`).

Uses:
- `app.api.routers` module exports.
- `register_exception_handlers`.
- `seed_source_profiles` + `seed_job_sources`.

Returns:
- `app` ASGI application object.

### `backend/app/api`
#### Routers (`backend/app/api/routers/*.py`)
Purpose:
- Define HTTP paths and method handlers.
- Parse request input and serialize response output.
- Delegate behavior to services.

Why:
- Keeps transport concerns separate from business logic.

How it interacts:
- Depends on service providers from `backend/app/api/deps.py`.

#### Dependency Injection (`backend/app/api/deps.py`)
Purpose:
- Build service instances with their repositories and collaborators.

Why:
- Centralizes wiring and reduces router coupling.

How it interacts:
- Routers call `Depends(get_..._service)`.
- Uses DB session provider + concrete repositories + registry objects.

#### Exception Handling (`backend/app/api/errors.py`)
Purpose:
- Map service exceptions to HTTP responses.

Mappings:
- `NotFoundError` -> `404`
- `ConflictError` -> `409`
- `ValidationServiceError` -> `422` with `detail` and `errors[]`

### `backend/app/schemas`
Purpose:
- Define request/response contracts using Pydantic.

Why:
- Typed API boundaries and consistent validation/serialization.

Examples:
- `job_source.py` for create/update/read of sources.
- `scrape_run.py` for run trigger/read payloads.
- `job_listing.py` for listing responses including `bookmark_status`.

### `backend/app/services`
Purpose:
- Application orchestration and business rules.

Key services:
1. `source_profile_service.py`: profile listing.
2. `job_source_service.py`: source CRUD + config validation.
3. `scrape_run_service.py`: scraping pipeline + run metrics.
4. `job_listing_service.py`: listing query + bookmark status hydration.
5. `job_bookmark_service.py`: bookmark upsert on a listing.
6. `export_service.py`: filtered export artifact generation.

Why:
- Encapsulates behavior independent of HTTP and SQL details.

### `backend/app/repositories`
Purpose:
- Encapsulate SQLAlchemy CRUD/query logic.

Why:
- Keeps query code outside services.
- Improves testability of service orchestration.

How it interacts:
- Services call repository interfaces from `interfaces.py`.
- Concrete classes use SQLAlchemy `Session`.

### `backend/app/db` and `backend/app/db/models`
Purpose:
- SQLAlchemy engine/session setup and ORM entities.
- Seed helpers for default profiles and default job sources.

Files:
- `session.py`: engine + `SessionLocal` + `get_db` generator.
- `base.py`: declarative base + naming conventions + timestamp mixin.
- `seeds.py`: app startup seeding logic.

### `backend/app/scrapers`
Purpose:
- Adapter contract + profile-specific scraping implementations.

Files:
- `contracts.py`: `ScraperAdapter` protocol and `ScrapedRecord`.
- `registry.py`: adapter lookup by profile code.
- `profiles/*.py`: Greenhouse, Lever, Custom HTML implementations.

Why:
- Isolates provider-specific parsing/fetch behavior.

### `backend/app/exporters`
Purpose:
- Format-specific export generation.

Files:
- `contracts.py`: `ExportArtifact`, `Exporter` protocol, shared columns.
- `csv_exporter.py` and `xlsx_exporter.py`.
- `registry.py`: resolve exporter by format.

Why:
- Avoid format branching inside service logic.

## Validation Model
1. Request-level validation via Pydantic schemas in routers.
2. Domain-specific config validation in `JobSourceConfigValidator`.
3. Service exceptions surfaced via global exception handlers.

## Database Access Model
- All DB interaction is via SQLAlchemy session (`Session`).
- Session is request-scoped from `get_db_session`.
- Services call repositories; repositories execute SQLAlchemy queries.
- Commit points are in service methods.

## Why Each Layer Exists
- Router: HTTP protocol boundary.
- Schema: contract and data shape validation.
- Service: orchestration/rules.
- Repository: persistence mechanics.
- Model: DB shape.
- Adapter/Exporter: external format/provider specialization.

## Known Limitations
- Some service methods use string status values directly (`"completed"`, `"failed"`) instead of enum wrappers.
- Scrape runs execute synchronously inside API request lifecycle.
