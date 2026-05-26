# FastAPI Example: API Key Management Endpoints

## Scenario
Implement `/api/v1/api-keys` create/list/revoke endpoints with strict response schemas, scoped auth, and auditability.

## Agent Collaboration
1. **architect**
   - Defines domain boundaries: key lifecycle service, audit service, auth boundary.
   - Specifies versioned contract and non-breaking error schema.
2. **fastapi**
   - Uses APIRouter per domain and Pydantic v2 request/response models.
   - Applies `Depends` for auth scope checks and DB session injection.
   - Adds SQLAlchemy persistence + Alembic migration for key metadata.
   - Ensures consistent envelope: `{data, error, meta}`.
3. **qa**
   - Tests create/list/revoke success, unauthorized scope, malformed payload, revoked-key behavior.
   - Adds backward compatibility contract tests from OpenAPI snapshots.
4. **code-review**
   - Requests explicit pagination metadata and deterministic error codes.
   - Approves after schema and tests are updated.

## Practical Deliverables
- OpenAPI-first spec with auth and error models.
- pytest suite (API + service layer + regression contracts).
- Release note: migration order and rollback procedure.

