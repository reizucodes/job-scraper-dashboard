# ADR Template

Use this template for lightweight, decision-focused architecture records.

## Template
```text
ADR-ID:

Status: Proposed | Accepted | Superseded

Context:

Decision:

Alternatives Considered:

Tradeoffs:

Consequences:

References:
```

## Usage Guidance
- Create an ADR when a decision changes architecture, contracts, boundaries, or operational risk.
- Keep each ADR focused on one decision.
- Prefer concise language with concrete rationale and consequences.

## Example Completed ADR
```text
ADR-ID: ADR-007

Status: Accepted

Context:
User-to-project assignment logic is duplicated across controllers and jobs.

Decision:
Centralize assignment rules in ProjectMembershipService and route all writes through it.

Alternatives Considered:
1) Keep logic in controllers
2) Introduce repository-heavy pattern

Tradeoffs:
Adds one service boundary but removes duplication and inconsistent authorization checks.

Consequences:
Improved testability and policy enforcement. Requires minor controller refactor.

References:
- Feature Spec: Team Assignment
- Security Review: AuthZ boundary checks
```

## Best Practices
- Link ADRs from feature specs and PR reviews.
- Update status to `Superseded` when replaced by a newer ADR.
- Include rollback/compatibility implications when contracts are affected.

