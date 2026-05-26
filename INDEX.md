# AI Agents Quick Start

This library is risk-scaled: use the lightest process that still protects quality and safety.

## Runtime Entry
Preferred initialization order:
1. `AGENTS.md`
2. `.ai/context/project-intelligence.md` (if present)
3. Other relevant `.ai/context/*` files
4. Relevant policies
5. Relevant workflow
6. Relevant agent
7. Repository inspection as needed

Startup guidance:
- Read `AGENTS.md` for global runtime instructions and governance baseline.
- Use this file (`INDEX.md`) to select risk path, templates, workflows, and participating agents.
- For runtimes that do not auto-load `AGENTS.md` (for example Claude Code, Cursor, Cline, or Roo Code), explicitly prompt the runtime to read `AGENTS.md` and `INDEX.md` before execution.

## Quick Start Matrix

| Change Size | Typical Examples | Template(s) | Workflow | Required Agents | Optional Agents | Gates/Policies |
|---|---|---|---|---|---|---|
| Tiny | Typo fixes, label changes, CSS tweaks, small validation message changes | `task.md` | `bugfix.md` or direct task execution | Stack agent | QA (optional for trivial non-functional edits) | DoD basics, runtime-safety/approval-levels if commands are risky |
| Small | Pagination, sorting, simple endpoint, small bug fix, UI enhancement | `task.md` | `feature.md` or `bugfix.md` | Stack agent, QA (recommended) | Code-review | Implementation + Quality gate, risk-classification, DoD |
| Medium | New module, new workflow, cross-domain feature, significant API changes | `feature-spec.md`, optional `adr.md` | `feature.md` | Architect, stack agent, QA, code-review | Product-spec, Security | Architecture + Implementation + Quality gates, risk-classification, DoD |
| High-Risk | Authentication, authorization, payments, sensitive data, public APIs, file uploads | `feature-spec.md`, `threat-model.md`, optional `adr.md` | `feature.md` (+ `release.md` when shipping) | Architect, Security, stack agent, QA, code-review | Product-spec, DevOps (required if deployment/ops impact) | Full gates including Release gate, secrets-management, runtime-safety, approval-levels |

`Stack agent` means one or more technology agents from `.ai/agents/`:
`laravel`, `vue`, `react`, `node-express`, `python`, `fastapi`.

## Recommended Flows

### Discovery (When Idea Is Still Vague)
`idea` -> `ideation` -> `product-spec` -> `architect` -> `stack agent`

### Tiny Change
`task` -> `stack agent`

### Small Change
`task` -> `stack agent` -> `qa`

### Medium Change
`feature-spec` -> `architect` -> `stack agent` -> `qa` -> `code-review`

### High-Risk Change
`feature-spec` -> `architect` -> `security` -> `stack agent` -> `qa` -> `code-review` -> `devops` (when release/ops impact exists)

Workflow entry points:
- Choose `bugfix.md` for defects/regressions.
- Choose `feature.md` for net-new behavior.
- Choose `refactor.md` for internal structural improvement without intended behavior change.
- Choose `release.md` for deployment/release readiness work.

## Agent Participation Guidance

### Ideation
Use when the problem or product direction is unclear and you need concept exploration before requirements are drafted.  
Usually skip when requirements are already clear and scoped.

### Product Spec
Use when requirements are unclear, business requirements are complex, multiple user stories exist, or significant planning is needed.  
Skip for small bug fixes, small enhancements, and routine implementation tasks.

### Architect
Use when boundaries change, significant design decisions are needed, new modules are introduced, or cross-domain changes occur.  
Usually skip for small fixes, minor enhancements, and routine CRUD work.

### Security
Use when authentication/authorization, sensitive data, public APIs, file uploads, payment functionality, or Medium+ risk exists.  
Usually skip for UI-only changes, simple refactors, and non-sensitive internal functionality.

### QA
Recommended for most implementation work.  
May be skipped only for trivial non-functional changes.

### Code Review
Recommended for Medium/High-risk work and shared codebases.  
Optional for small personal changes.

### DevOps
Required only when deployment, infrastructure, or operational behavior changes.  
Not mandatory for routine feature work.

## Template Selection
- Use `task.md` for quick daily work.
- Use `feature-spec.md` for larger or ambiguous work.
- Use `threat-model.md` for security-sensitive changes.
- Use `adr.md` when decisions alter architecture/contracts.

## Practical Rule
Start small, escalate only when risk or complexity increases.

## Workflow Automation Model
Workflow progression should behave as:

Prompt  
-> Ideation  
-> Product Spec  
-> Architect  
-> Implementation Plan  
-> Implementation  
-> QA  
-> Code Review

User interaction is only required when a Decision Gate is triggered.

- Agents should refine and structure work automatically between stages.
- Stage outputs should automatically become inputs to the next stage.
- Decision Gates are used only for meaningful human-judgment choices.
- Decision behavior is defined in `.ai/policies/decision-gates.md`.

## Policy Map
- Decision flow: `.ai/policies/decision-gates.md`
- Approval boundaries: `.ai/policies/approval-levels.md`
- Runtime safety execution rules: `.ai/policies/runtime-safety.md`
- Risk classification: `.ai/policies/risk-classification.md`
- Completion baseline: `.ai/policies/definition-of-done.md`
- Quality gates: `.ai/policies/quality-gates.md`
- Secrets handling: `.ai/policies/secrets-management.md`

## Project Knowledge Base
`.ai/context/*` acts as a repository-specific knowledge layer that:
- reduces repeated repository discovery
- preserves architectural understanding
- captures project conventions
- accelerates onboarding for AI runtimes
- improves implementation consistency across sessions

If `.ai/context/` exists, treat all files inside it as repository-specific knowledge artifacts.

Consult these files before:
- architecture work
- implementation work
- refactoring
- testing
- security reviews
- release activities

Knowledge files help:
- reduce repeated repository discovery
- preserve architectural context
- preserve project conventions
- improve implementation consistency
- accelerate onboarding for AI runtimes

Guidance:
- Knowledge files are accelerators, not absolute truth.
- Repository source code remains the ultimate source of truth.
- When conflicts occur, prefer current repository evidence.
- Knowledge files should be updated after significant repository changes.
- Before implementation, if `.ai/context/confidence-gates.md` exists, use it to classify the requested change and determine required pre-implementation checks.
- Confidence gates are especially important for:
  - authentication/authorization
  - sensitive data handling
  - public APIs or external contracts
  - data model or persistence changes
  - external integrations
  - background jobs, queues, or scheduled tasks
  - configuration/environment changes
  - deployment/release changes
  - security-sensitive changes

Knowledge precedence:
1. Current repository source code
2. Repository configuration and manifests
3. Repository intelligence files
4. Generated assumptions

If conflicts exist:
- Prefer repository evidence.
- Update intelligence files accordingly.

Refresh knowledge artifacts after:
- architectural changes
- major dependency changes
- integration changes
- domain-model changes
- large refactors
- release process changes

Example structure:

```txt
.ai/context/
├── project-intelligence.md
├── architecture.md
├── domain-model.md
├── coding-patterns.md
├── integrations.md
├── testing-strategy.md
├── technical-debt.md
└── confidence-gates.md
```

## Examples
Use `examples/*/README.md` for scenario references that show collaboration patterns by stack, not complete generated implementation artifacts.

## Future Extensions (Optional)
- `./.ai/skills/`: extract shared guidance only when duplication appears across three or more locations.
- `./.ai/hooks/`: automate only repeatable, high-frequency manual tasks with reliable triggers.
