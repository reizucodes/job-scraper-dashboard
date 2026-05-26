# Bugfix Workflow

## Purpose
Diagnose defects quickly, fix root cause, and prevent regression.

## Participating Agents
Stack agent, `qa`, `code-review`, optional `architect`, optional `security`.

Participation scales by risk path below; not all agents are used for every change.

## Execution Order
Use the risk paths below to choose the right depth. The sequence below reflects the structured flow used when bug impact is beyond low risk.

Implementation planning ownership:
- `architect` owns technical implementation planning for non-trivial/boundary-impacting fixes.
- stack agent owns stack-specific implementation steps and execution details.

1. Reproduce issue and gather failing evidence.
2. Identify root cause and affected surfaces.
3. Implement minimal safe fix.
4. Add regression tests and validate edge behavior.
5. Run review gate and release decision.

## Stage Progression Rules
- Stages should continue automatically whenever no Decision Gate is triggered.
- Stage outputs automatically become inputs to the next stage.
- Do not pause only because a stage completed.
- Only Recommendation Decisions and Approval Decisions may pause execution.
- Approval Decisions must follow `.ai/policies/approval-levels.md`.
- Decision Gate behavior must follow `.ai/policies/decision-gates.md`.

## Deliverables
- Root cause analysis
- Fix summary
- Regression test coverage
- Risk assessment

## Success Criteria
- Original defect no longer reproducible.
- Regression suite updated and passing.
- No unresolved high-severity findings.

## Escalation Rules
- Repeated defects across boundaries -> `architect`.
- Runtime instability risk -> `devops`.

## Recommended Usage
Use for production incidents, QA-found defects, and contract-breaking bugs.

## Low Risk Path
- **Templates:** `task.md`.
- **Required Agents:** stack agent.
- **Recommended Agents:** `qa`.
- **Optional Agents:** `code-review`.
- **Gates:** Implementation + Quality (lightweight for trivial fixes).
- **Policies:** risk-classification, definition-of-done.

## Medium Risk Path
- **Templates:** `task.md` or `feature-spec.md` if scope expands.
- **Required Agents:** stack agent, `qa`, `code-review`.
- **Optional Agents:** `architect`, `security` (when auth/data/public API concerns exist).
- **Gates:** Implementation + Quality.
- **Policies:** risk-classification, quality-gates, approval-levels/runtime-safety.

## High Risk Path
- **Templates:** `feature-spec.md` + `threat-model.md` when security-sensitive.
- **Required Agents:** stack agent, `qa`, `code-review`, `security`.
- **Optional Agents:** `architect`.
- **DevOps:** required when release/deployment risk is introduced.
- **Gates:** Implementation + Quality + Release (when production readiness is affected).
- **Policies:** all relevant governance policies, especially secrets-management.

## Agent Handoffs
- QA -> Stack: deterministic repro and expected behavior.
- Security -> Stack/QA (conditional): security findings, risk impact, required validation checks.
- Stack -> Code-review: diff rationale + test proof.

## Gate Selection
Gate requirements vary by risk level.

- **Low Risk:** lightweight validation, Definition of Done, and applicable safety policies.
- **Medium Risk:** Implementation Gate + Quality Gate.
- **High Risk:** Implementation + Quality gates, plus Release Gate when production readiness is affected.

See Low/Medium/High risk paths above.

## Risk Assessment
- Perform at bug triage and re-evaluate after root cause is identified.
- Use `.ai/policies/risk-classification.md`.
- Recommend `security` involvement when auth/authz, sensitive data, public APIs, file uploads, payment flows, or Medium+ risk is present.

## Approval Requirements
- Level 1 approvals for dependency, migration, or destructive file actions.
- Level 2 actions require explicit user command only.

## Handoff Requirements
- QA -> Stack: repro steps, expected/actual behavior, severity/priority.
- Security -> Stack/QA (conditional): risk findings, required mitigations, validation scope.
- Stack -> QA: root cause, fix scope, regression tests.
- QA -> Code-review: verification results + residual risks.

## Exit Criteria
- Defect fixed and no longer reproducible.
- Regression tests updated/passing.
- Required gates passed and DoD satisfied.
