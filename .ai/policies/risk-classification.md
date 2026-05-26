# Risk Classification Policy

## Purpose
Provide consistent impact-based risk language across planning, implementation, QA, review, and release decisions.

## Levels

## Low
- **Description:** Minor localized change with low blast radius.
- **Examples:** UI copy fix, non-critical refactor, doc-only API clarification.
- **Required Reviews:** Stack agent self-review; QA spot checks.
- **Required Approvals:** Level 0 actions only unless state-changing operations occur.
- **Workflow Implications:** Standard gates, lighter regression scope.

## Medium
- **Description:** Moderate functional impact or shared module change.
- **Examples:** New endpoint in existing service, state management changes, migration with simple rollback.
- **Required Reviews:** QA review + code-review.
- **Required Approvals:** Level 1 for dependency/migration/state-changing operations.
- **Workflow Implications:** Full Architecture/Implementation/Quality gates.

## High
- **Description:** Significant business/system impact, sensitive data/auth or multi-service coupling.
- **Examples:** Auth model changes, cross-service contract changes, complex schema migrations.
- **Required Reviews:** Architect + QA + code-review + devops readiness input.
- **Required Approvals:** Level 1 actions must be explicitly approved; Level 2 prohibited without explicit user command.
- **Workflow Implications:** Security-focused QA and release gate mandatory.

## Critical
- **Description:** Potential severe outage, data loss, security breach, or production instability.
- **Examples:** Production data migration with irreversible steps, auth credential handling changes, critical infrastructure operations.
- **Required Reviews:** Architect + QA + code-review + devops, with documented escalation.
- **Required Approvals:** Level 2 explicit user command required for execution-sensitive actions.
- **Workflow Implications:** Incident-level controls; release blocked until all mitigations are verified.

## Escalation Rules
1. Escalate to architect when domain boundaries or contract compatibility are uncertain.
2. Escalate to devops for runtime/deployment risk at high or critical levels.
3. Escalate to code-review for unresolved security/performance concerns.
4. Reclassify risk if new evidence increases blast radius.

