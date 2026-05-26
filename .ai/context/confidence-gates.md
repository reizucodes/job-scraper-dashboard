# Confidence Gates

## Purpose
Provide pre-implementation confidence guidance for this repository so future changes target the right files/tests before coding.

## Confidence Scale
- High: Strong evidence and repeatable patterns.
- Medium: Good evidence with some coupling/edge risk.
- Low: Limited evidence; requires deeper inspection.
- Unconfirmed: Insufficient evidence.

## Change Type Confidence Matrix
- Standard feature change
  - Confidence level: High
  - Why: Clear router/service/repository boundaries and tests exist.
  - Required files or areas to inspect: `backend/app/api/routers`, `backend/app/services`, `frontend/src/stores`, `frontend/src/views`
  - Required tests/checks: `backend pytest`, `frontend vitest`, `frontend build`
  - Approval gate recommendation: Standard implementation + quality gate.
- Bug fix
  - Confidence level: High
  - Why: Existing tests are comprehensive for MVP paths.
  - Required files or areas to inspect: failing module + related tests.
  - Required tests/checks: targeted tests + full suite.
  - Approval gate recommendation: Standard.
- Refactor
  - Confidence level: Medium
  - Why: Cross-layer coupling (DTO/store/view) can break integration.
  - Required files or areas to inspect: schemas, API modules, stores, views.
  - Required tests/checks: backend tests + frontend tests/build.
  - Approval gate recommendation: Architecture review if contracts move.
- Data model or persistence change
  - Confidence level: Medium
  - Why: Alembic + SQLAlchemy are structured but model changes affect dedupe/export flows.
  - Required files or areas to inspect: `backend/app/db/models`, `backend/alembic`, services using listing/raw models.
  - Required tests/checks: migration upgrade test + backend suite + smoke export.
  - Approval gate recommendation: Migration/rollback notes required.
- Authentication/authorization change
  - Confidence level: Low
  - Why: No auth baseline currently implemented.
  - Required files or areas to inspect: all routers/services and frontend API flows.
  - Required tests/checks: security-focused API tests + regression suites.
  - Approval gate recommendation: Security + architecture gate.
- External integration change
  - Confidence level: Medium
  - Why: Scraper adapters isolated, but only fixture-driven paths are validated.
  - Required files or areas to inspect: `backend/app/scrapers`, `scrape_run_service`.
  - Required tests/checks: adapter contract tests + orchestration integration tests.
  - Approval gate recommendation: Integration risk review.
- Public API or interface contract change
  - Confidence level: Medium
  - Why: Frontend strongly depends on backend DTO shapes.
  - Required files or areas to inspect: `backend/app/schemas`, `frontend/src/api/types.ts`, stores/views.
  - Required tests/checks: backend + frontend contract regression.
  - Approval gate recommendation: Architecture gate.
- Background job / queue / scheduled task change
  - Confidence level: Low
  - Why: Current architecture is synchronous/manual only.
  - Required files or areas to inspect: scrape service, run metrics model, ops/deployment docs.
  - Required tests/checks: queue integration tests + migration checks.
  - Approval gate recommendation: Architecture + release gate.
- Configuration or environment change
  - Confidence level: Medium
  - Why: Both apps rely on env/tool configs and build scripts.
  - Required files or areas to inspect: `backend/app/core/config.py`, package/tooling configs.
  - Required tests/checks: startup smoke + build/test suites.
  - Approval gate recommendation: Standard.
- Testing-only change
  - Confidence level: High
  - Why: test layout and patterns are clear.
  - Required files or areas to inspect: `backend/tests`, `frontend/tests`.
  - Required tests/checks: full relevant test suite.
  - Approval gate recommendation: Standard.
- Deployment/release change
  - Confidence level: Unconfirmed
  - Why: no deployment pipeline manifests observed in repo.
  - Required files or areas to inspect: Unconfirmed.
  - Required tests/checks: Define release process first.
  - Approval gate recommendation: Release governance definition required.
- Security-sensitive change
  - Confidence level: Medium
  - Why: security model is simple now, but no auth means high exposure risk if deployed.
  - Required files or areas to inspect: all API boundaries, error handling, configuration.
  - Required tests/checks: security review + regression + integration checks.
  - Approval gate recommendation: Security gate.

## Required Pre-Implementation Checks
- Confirm affected backend DTOs and frontend API types stay aligned.
- Confirm migration requirements before model/persistence edits.
- Confirm existing tests cover intended behavior and extend where missing.

## High-Risk Change Gates
- Auth/Authz introduction: architecture + security gate.
- Async/background scrape processing: architecture + release readiness gate.
- Contract-breaking API changes: architecture gate + frontend integration gate.

## Files to Inspect by Change Type
- Backend feature work: `backend/app/api/routers`, `backend/app/services`, `backend/app/repositories`, `backend/app/schemas`
- Persistence changes: `backend/app/db/models`, `backend/alembic/versions`
- Scrape pipeline changes: `backend/app/scrapers`, `backend/app/services/scrape_run_service.py`, `backend/app/services/dedupe_service.py`
- Frontend integration changes: `frontend/src/api`, `frontend/src/stores`, `frontend/src/views`, `frontend/src/components/shared`

## Approval Gate Recommendations
- Standard MVP changes: implementation + quality checks.
- Boundary/contract/security changes: architecture/security reviews before implementation.

## Notes for Future Agents
- Treat `backend/app/schemas` and `frontend/src/api/types.ts` as joint contract surface.
- Keep routers thin and preserve service/repository boundaries.
- Preserve deterministic fixture-based scraper tests unless explicitly expanding integration scope.
