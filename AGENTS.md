# AI Agents Root Instructions

## Engineering Principles
- Apply SOLID, DRY, and KISS in all recommendations.
- Prefer maintainability and testability over clever abstractions.
- Use composition over inheritance unless inheritance clearly improves clarity.
- Favor explicit contracts (types, interfaces, schemas) over implicit behavior.

## Coding Standards
- Follow language/framework conventions first.
- Keep modules small and focused with clear ownership boundaries.
- Require strong typing:
  - PHP: `declare(strict_types=1);`, typed params/returns/properties.
  - TypeScript: no `any` unless explicitly justified.
  - Python: type hints on public functions and models.
- Introduce abstractions only when duplication or complexity justifies them.

## Communication Standards
- Be direct, factual, and implementation-oriented.
- State assumptions and tradeoffs explicitly.
- When blocked, explain what is missing and propose next concrete action.
- Prefer actionable checklists over generic guidance.

## Documentation Expectations
- Document architecture decisions, data contracts, and operational impacts.
- Keep API docs aligned with implementation and tests.
- Include migration/rollback notes for data or contract changes.

## Testing Expectations
- Define test scope before implementation.
- Cover success paths, validation failures, edge cases, error handling, and regressions.
- Prefer deterministic tests with clear setup/teardown.
- Match stack defaults: PHPUnit/Vitest/pytest as applicable.

## Review Expectations
- Review for correctness, maintainability, security, performance, and test depth.
- Flag risky coupling, hidden side effects, and missing validation.
- Require clear diff-level rationale for non-trivial architecture choices.

## Security Principles
- Validate all untrusted input.
- Enforce authn/authz close to domain boundaries.
- Apply least privilege for credentials and services.
- Avoid leaking sensitive data in logs, errors, and telemetry.

## Architecture Principles
- Design around domain boundaries and explicit interfaces.
- Keep infra concerns separate from business logic.
- Favor backward-compatible API changes and versioning discipline.
- Surface performance tradeoffs with measurable impacts.

## Output Formatting Rules
`AGENTS.md` defines the canonical response wrapper for all agents and workflows.
Agent-specific output sections describe what content must be included, but they must be organized inside this global structure.

All agents must return output in this order:
1. **Context & Assumptions**
2. **Proposed Approach**
3. **Implementation Details**
4. **Testing Plan**
5. **Risks & Tradeoffs**
6. **Handoffs / Next Agent Inputs**

## Governance Policy References
- `.ai/policies/approval-levels.md`
- `.ai/policies/decision-gates.md`
- `.ai/policies/runtime-safety.md`
- `.ai/policies/quality-gates.md`
- `.ai/policies/risk-classification.md`
- `.ai/policies/definition-of-done.md`
- `.ai/policies/secrets-management.md`

All agents and workflows must apply these policies consistently.

## Workflow Scaling Philosophy
Scale process according to risk:
- Fast path for small work.
- Structured path for complex work.
- Security path for sensitive work.

Use `INDEX.md` as the primary entrypoint for selecting templates, workflows, and agent participation by change size.

## Security and Product Discovery
- Engage `product-spec` before architecture when requirements are unclear or incomplete.
- Engage `security` when any of the following apply:
  - authentication or authorization changes,
  - sensitive data handling,
  - public API exposure,
  - file upload support,
  - payment-related flows,
  - Medium or higher risk classification.
