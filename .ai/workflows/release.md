# Release Workflow

## Purpose
Prepare and execute production releases with controlled risk and rollback readiness.

## Participating Agents
Stack agent(s), `qa`, `code-review`, `devops`, optional `architect`, optional `security`.

Participation scales by risk path below; not all agents are used for every release scope.

## Execution Order
Use the risk paths below to choose the right depth. The sequence below reflects the structured flow used for medium/high-risk release work.

Implementation planning ownership:
- `architect` owns technical implementation planning when release scope includes non-trivial boundary/contract changes.
- stack agent owns stack-specific implementation/release execution steps.

1. Confirm scope, changes, and compatibility impacts.
2. Validate test suite and regression pass.
3. Run release readiness review (security/performance/observability).
4. Execute staged deployment strategy.
5. Monitor, verify, and close release.

## Stage Progression Rules
- Stages should continue automatically whenever no Decision Gate is triggered.
- Stage outputs automatically become inputs to the next stage.
- Do not pause only because a stage completed.
- Only Recommendation Decisions and Approval Decisions may pause execution.
- Approval Decisions must follow `.ai/policies/approval-levels.md`.
- Decision Gate behavior must follow `.ai/policies/decision-gates.md`.

## Deliverables
- Release checklist
- Rollback plan
- Monitoring/alert plan
- Post-release verification summary

## Success Criteria
- Deployment completed without critical incident.
- SLO-impacting errors absent or within threshold.
- Rollback path verified before release.

## Escalation Rules
- Critical production anomaly -> immediate rollback and incident channel.
- Contract mismatch -> `architect` + relevant stack agent.

## Recommended Usage
Use for every production release, especially API and schema changes.

## Low Risk Path
- **Templates:** `task.md` or release notes summary.
- **Required Agents:** stack agent.
- **Recommended Agents:** `qa`, `code-review`.
- **Optional Agents:** `devops` for simple internal/non-prod release checks.
- **Gates:** Quality + Release (lean checklist for low-risk changes).
- **Policies:** approval-levels, runtime-safety, definition-of-done.

## Medium Risk Path
- **Templates:** `feature-spec.md` (or equivalent change record), `test-plan.md`.
- **Required Agents:** stack agent, `qa`, `code-review`, `devops`.
- **Optional Agents:** `architect`, `security`.
- **Gates:** Quality + Release; Architecture gate if contracts/boundaries changed.
- **Policies:** risk-classification, quality-gates, runtime-safety, approval-levels.

## High Risk Path
- **Templates:** `feature-spec.md`, `threat-model.md`, rollback plan artifact.
- **Required Agents:** stack agent, `qa`, `code-review`, `devops`, `security`.
- **Optional Agents:** `architect` (required if boundary or contract decisions changed).
- **Gates:** Architecture (when needed) + Quality + Release (strict).
- **Policies:** all governance policies, especially secrets-management.

## Agent Handoffs
- Stack -> DevOps: artifacts, migration steps, health checks.
- QA -> DevOps: go/no-go test evidence and residual risk.

## Gate Selection
Gate requirements vary by risk level.

- **Low Risk:** lean Quality + Release validation, Definition of Done, and applicable safety policies.
- **Medium Risk:** Quality + Release gates (Architecture Gate when contracts/boundaries changed).
- **High Risk:** strict Quality + Release governance, plus Architecture Gate when boundary/contract decisions are involved.

See Low/Medium/High risk paths above.

## Risk Assessment
- Risk classification required before release decision.
- High/Critical risk requires explicit mitigation checklist and escalation.
- Recommend `security` review for releases involving auth/authz, sensitive data paths, public APIs, file uploads, payment functionality, or Medium+ unresolved security findings.

## Approval Requirements
- Level 1 approvals required for release-prep state changes.
- Level 2 explicit user instruction required for production deployment/destructive operations.

## Handoff Requirements
- Stack -> DevOps: release artifact list, migration plan, rollback commands, health checks.
- QA -> DevOps: pass/fail matrix, unresolved risks, severity summary.
- Code-review -> DevOps: approval status and blocking findings.

## Exit Criteria
- Release Gate fully passed.
- Deployment and rollback plans documented.
- Observability checks active.
- No unresolved critical defects/findings.
