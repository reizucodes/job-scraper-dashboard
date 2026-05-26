# Definition of Done Policy

## Purpose
Define minimum completion standards before work is considered done in any workflow.

## Global Requirements
- Implementation complete for approved scope.
- Acceptance criteria satisfied.
- Documentation updated (contracts, behavior, ops notes as needed).
- Tests added for changed behavior.
- Required tests passing.
- No required lint/type-check failures.
- Security considerations reviewed.
- Architecture consistency maintained with approved boundaries.

## Laravel
- PHPUnit feature tests added/updated.
- PHPUnit unit tests added/updated where domain logic changes.
- Validation coverage via Form Requests or equivalent.
- API documentation/OpenAPI references updated.

## Vue
- Component and composable tests (Vitest) updated.
- Accessibility validation performed (keyboard/labels/focus/semantics).
- State management behavior validated (Pinia/local state transitions).

## React
- Component and hook tests (Vitest) updated.
- Accessibility validation performed.
- State transitions and error/loading behavior validated.

## Node Express
- Endpoint behavior tests added/updated.
- Validation tests for malformed/invalid requests.
- Error handling contract tested (status + stable error shape).

## FastAPI
- Request model validation verified.
- Response model validation verified.
- OpenAPI output verified for changed endpoints.
- API contract compatibility validated (including error responses).

## Python
- pytest coverage added for changed behavior.
- Type checking expectations satisfied.
- Documentation and usage notes updated for scripts/services.

