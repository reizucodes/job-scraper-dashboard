# Refactor Workflow

## Purpose
Improve internal code quality without changing external behavior.

## Participating Agents
`architect` (if broad scope), stack agent, `qa`, `code-review`.

Participation scales by risk path below; not all agents are used for every change.

## Execution Order
Use the risk paths below to choose the right depth. The sequence below reflects the structured flow used when refactor scope is beyond low risk.

Implementation planning ownership:
- `architect` owns technical implementation planning for non-trivial/boundary-impacting refactors.
- stack agent owns stack-specific implementation steps and execution details.

1. Define refactor scope and protected behavior.
2. Baseline tests and key metrics.
3. Refactor incrementally behind passing tests.
4. Validate no behavior drift.
5. Review complexity and maintainability deltas.

## Stage Progression Rules
- Stages should continue automatically whenever no Decision Gate is triggered.
- Stage outputs automatically become inputs to the next stage.
- Do not pause only because a stage completed.
- Only Recommendation Decisions and Approval Decisions may pause execution.
- Approval Decisions must follow `.ai/policies/approval-levels.md`.
- Decision Gate behavior must follow `.ai/policies/decision-gates.md`.

## Deliverables
- Refactor scope statement
- Before/after architecture notes
- Test and regression evidence
- Risk log

## Success Criteria
- Behavior preserved.
- Complexity and maintainability improved measurably.
- Coverage unchanged or improved.

## Escalation Rules
- Scope creep or architecture drift -> `architect`.
- Performance regression -> stack agent + `qa`.

## Recommended Usage
Use for debt reduction, module simplification, and coupling reduction.

## Low Risk Path
- **Templates:** `task.md`.
- **Required Agents:** stack agent.
- **Recommended Agents:** `qa`.
- **Optional Agents:** `code-review`.
- **Gates:** Implementation + Quality (lightweight parity checks).
- **Policies:** risk-classification, definition-of-done.

## Medium Risk Path
- **Templates:** `task.md` or `feature-spec.md` for larger scope.
- **Required Agents:** stack agent, `qa`, `code-review`.
- **Optional Agents:** `architect`.
- **Gates:** Implementation + Quality; Architecture gate if boundaries shift.
- **Policies:** risk-classification, quality-gates, approval-levels/runtime-safety.

## High Risk Path
- **Templates:** `feature-spec.md`, `adr.md` recommended.
- **Required Agents:** `architect`, stack agent, `qa`, `code-review`.
- **Optional Agents:** `security` when sensitive/auth/public API surfaces are touched.
- **DevOps:** required only when operational/deployment behavior changes.
- **Gates:** Architecture + Implementation + Quality (+ Release when needed).
- **Policies:** full governance set as applicable.

## Agent Handoffs
- Architect -> Stack: boundary constraints.
- Stack -> QA: areas with highest regression risk.

## Gate Selection
Gate requirements vary by risk level.

- **Low Risk:** lightweight parity validation, Definition of Done, and applicable safety policies.
- **Medium Risk:** Implementation Gate + Quality Gate (Architecture Gate only when boundaries/contracts shift).
- **High Risk:** Architecture + Implementation + Quality gates, plus Release Gate when production readiness is affected.

See Low/Medium/High risk paths above.

## Risk Assessment
- Classify risk before refactor starts and after major structural changes.
- Use `.ai/policies/risk-classification.md`.
- Include `security` review when any of the following apply:
  - authentication or authorization surfaces are touched,
  - sensitive data handling changes,
  - public API behavior changes,
  - file upload behavior changes,
  - risk classification is Medium or higher.

## Approval Requirements
- Level 1 approval required for destructive operations (file deletions/major moves/dependency changes).
- Level 2 actions require explicit user command.

## Handoff Requirements
- Architect -> Stack: protected behaviors + constraints + ADR notes.
- Stack -> QA: changed internals, preserved contracts, regression targets.
- QA -> Code-review: parity verification and risk outcomes.

## Exit Criteria
- Behavior preserved with passing tests.
- Maintainability/complexity improvements documented.
- Required gates passed and DoD satisfied.
