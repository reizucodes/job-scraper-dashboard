# Quality Gates Policy

## Purpose
Prevent unsafe workflow progression with mandatory gate validation for the gates selected by workflow and risk path.

Workflow files determine gate depth/applicability by risk level (low/medium/high). Once a gate is selected, its requirements are mandatory.
For low-risk work, evidence may be lightweight (for example: focused checks, targeted tests, concise validation notes) while still meeting Definition of Done and applicable safety policies.

## Architecture Gate
### Requirements
- Feature specification exists.
- Acceptance criteria defined.
- Risks identified.
- Architecture documented.
- API contracts defined when applicable.

### Failure Behavior
Stop progression and request missing inputs before implementation starts.

### Example
A new endpoint is proposed without response/error contract. Gate fails until contract is defined.

## Implementation Gate
### Requirements
- Feature implementation complete for agreed scope.
- Tests added for changed behavior.
- Documentation updated.
- No compilation/build errors.
- No failing required tests.

### Failure Behavior
Return implementation deficiencies and block QA handoff until resolved.

### Example
Feature compiles locally but integration tests fail on validation edge case. Gate fails.

## Quality Gate
### Requirements
- QA review complete.
- Security review complete when risk is medium+ or auth/data boundaries changed.
- Critical defects resolved.
- Acceptance criteria satisfied.

### Failure Behavior
Block merge/release progression.

### Example
QA finds authorization bypass (high severity). Gate remains blocked until fix + retest.

## Release Gate
### Requirements
- Documentation complete.
- Required tests passing.
- Code review completed.
- Deployment plan documented.
- Rollback plan documented and validated.

### Failure Behavior
Block release readiness status.

### Example
No rollback for schema migration is documented. Release gate fails.
