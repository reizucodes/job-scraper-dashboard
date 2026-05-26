# Decision Gates Policy

## Purpose
Reduce unnecessary user interruption while preserving user control over meaningful product, UX, architecture, scope, security, cost, and complexity decisions.

## Decision Gates

## Auto Decisions
Agent proceeds automatically.

Use when:
- one clearly superior solution exists,
- industry best practice is obvious,
- decision impact is low,
- decision affects implementation details only.

Examples:
- folder structure choices,
- naming conventions,
- TypeScript typing patterns,
- Vue composition patterns,
- component splitting,
- internal refactor structure.

Behavior:
- proceed without user interruption,
- carry outputs directly into the next stage.

## Recommendation Decisions
Agent pauses and requests user input.

Use when:
- multiple viable solutions exist,
- tradeoffs materially affect outcome,
- product direction changes,
- architecture direction changes,
- scope differs significantly.
- security design choices require human judgment but do not trigger approval-level operations.

Security design choice examples (Recommendation Decisions):
- JWT vs session authentication,
- RBAC vs ABAC,
- local secrets vs cloud secret manager strategy,
- token lifetime strategy,
- public vs private API exposure model.

Required format:
```text
Decision Required
Context:
...

Option A
Pros:
Cons:

Option B
Pros:
Cons:

Recommended:
...

Please choose:
1)
2)
```

Behavior:
- pause workflow until user responds,
- resume automatically after selection.

## Approval Decisions
Agent must stop and wait for explicit approval.

Examples:
- git commits,
- git pushes,
- branch deletion,
- dependency upgrades,
- file deletion,
- database migrations,
- production actions,
- security-sensitive operations that map to explicit approval-level actions.

Security operation examples (Approval Decisions):
- secret rotation,
- credential replacement,
- security configuration deletion,
- production security changes,
- production deployments,
- repository modifications that require approval-level review.

Behavior:
- follow `.ai/policies/approval-levels.md`.

Rule:
- security design choices -> Recommendation Decision.
- security-affecting operations requiring approval-level actions -> Approval Decision.

## Decision Resolution Rule
When a user selects an option from a Recommendation Decision:
- mark the decision as resolved,
- continue workflow progression automatically,
- treat the selected option as authoritative input.

Do not reopen the same decision unless:
- new material information emerges,
- requirements materially change,
- the user explicitly requests reconsideration.
