# Build Project Intelligence Workflow

## Purpose
Generate and maintain repository-specific intelligence artifacts in `.ai/context/` to preserve architecture, conventions, domain knowledge, integrations, testing strategy, technical debt, and implementation guidance across AI sessions.

This workflow is language/framework/runtime agnostic and designed as a repository-local, human-readable knowledge layer with no external retrieval infrastructure.

## Scope
- Create `.ai/context/` if it does not exist.
- Create or refresh `.ai/context/project-intelligence.md` as the authoritative summary artifact.
- Optionally create or refresh specialized artifacts when repository complexity justifies separation:
  - `.ai/context/architecture.md`
  - `.ai/context/domain-model.md`
  - `.ai/context/coding-patterns.md`
  - `.ai/context/integrations.md`
  - `.ai/context/testing-strategy.md`
  - `.ai/context/technical-debt.md`
  - `.ai/context/confidence-gates.md`
- Perform evidence-based repository analysis only.
- Do not modify application source code.

## Refresh Mode
When intelligence files already exist:
- Read existing intelligence artifacts before analysis.
- Preserve valid findings.
- Update stale findings.
- Remove disproven findings.
- Add newly discovered findings.
- Maintain evidence references where possible.
- Recalculate confidence levels.
- Avoid discarding useful historical context unnecessarily.

This workflow supports both initial intelligence generation and incremental intelligence refresh without requiring separate workflows.

## Constraints
- Do not invent architecture.
- Do not rewrite the project.
- Do not create new conventions unless requested.
- Do not expose secrets.
- Do not include credentials.
- Do not install dependencies without approval.
- Do not execute destructive commands.

## Confidence Definitions
Classify major findings with one of the following confidence levels where appropriate:

### High
- Supported by multiple repository sources.
- Strong and consistent evidence.

### Medium
- Supported by limited evidence.
- Likely accurate but incomplete.

### Low
- Weak evidence.
- Requires validation.

### Unconfirmed
- Insufficient evidence.
- Cannot be confidently asserted.

## Phases

### 1) Discovery
- Inspect repository tree and key documentation/configuration files.
- Identify likely architecture, modules, operational boundaries, and implementation surfaces.
- Record repository file references for all major findings.

### 2) Stack and Runtime Detection
- Infer and document:
  - Primary language(s)
  - Framework(s)
  - Runtime environment
- Base findings on manifests, lockfiles, toolchain configs, runtime configs, and deployment descriptors.
- Mark any uncertain finding as `Unconfirmed`.

### 3) Architecture Mapping
- Infer and document:
  - Repository structure
  - Architecture style
  - Data flow boundaries
  - Internal service/component boundaries
- Tie every architectural statement to concrete file evidence.
- Mark ambiguous topology claims as `Unconfirmed`.

### 4) Domain and Feature Mapping
- Infer and document:
  - Business domains
  - Domain model / business concepts
  - Feature inventory
- Prefer explicit evidence from routes/controllers/services/docs/tests.
- Mark inferred but weakly-supported feature claims as `Unconfirmed`.

### 5) Pattern Recognition
- Infer and document:
  - Coding conventions
  - Design patterns
  - API conventions
  - Data persistence model
  - Authentication and authorization model
  - External integrations
- Use repeated code and configuration patterns as evidence.
- Do not elevate single-instance implementation details into global conventions unless evidence is broad enough.

### 6) Testing and Quality Mapping
- Infer and document:
  - Testing strategy
  - Test organization and scope
  - Quality gates and CI signals
- Reference testing frameworks, test directories, and CI workflow files.

### 7) Risk and Technical Debt Mapping
- Infer and document:
  - Technical debt
  - Risk areas
  - Known edge cases
- Capture fragile patterns, coupling hotspots, missing validation, weak test coverage, and operational risk indicators.
- Mark speculative risk claims as `Unconfirmed`.

### 8) Report Generation
- Generate `.ai/context/project-intelligence.md` using the exact report structure below.
- Include evidence index entries that map claims to repository files.
- Include confidence calibration for major sections.
- Generate specialized artifacts only when sufficient repository complexity justifies separation.
- Generate `.ai/context/confidence-gates.md` when meaningful risk differences exist across change types, domains, modules, integrations, or operational surfaces.
- Avoid fragmentation for small repositories and keep `project-intelligence.md` as the authoritative summary.

### 9) Review Checklist
- Confirm `.ai/context/` exists.
- Confirm `.ai/context/project-intelligence.md` exists.
- Confirm no application source files were modified.
- Confirm uncertain findings are explicitly marked `Unconfirmed`.
- Confirm all major claims have file-reference evidence.
- Confirm no secrets or credentials are present in the report.

## Required Report Structure
Use this structure for `.ai/context/project-intelligence.md`:

```md
# Project Intelligence Report

## Metadata
- Generated date
- Repository name
- Primary stack
- Confidence level
- Files inspected summary

## Executive Summary
## Stack and Runtime
## Repository Structure
## Architecture Overview
## Domain Model / Business Concepts
## Feature Inventory
## Data Persistence
## API / Interface Conventions
## Authentication and Authorization
## External Integrations
## Coding Patterns
## Testing Strategy
## Build, Tooling, and Deployment
## Security and Risk Notes
## Technical Debt and Fragile Areas
## AI Implementation Guidance
## Open Questions
## Evidence Index
```

## AI Implementation Guidance Requirements
The `AI Implementation Guidance` section must include:
- Preferred code locations.
- Existing architectural boundaries.
- Existing abstractions to reuse.
- Repeated implementation patterns.
- Patterns to avoid.
- Testing expectations.
- Risk-sensitive components.
- Refactor cautions.
- Approval gate triggers.

This guidance should explicitly optimize future coding-agent behavior.

## Confidence Gates Artifact (Optional Specialized Artifact)
Generate `.ai/context/confidence-gates.md` when the repository has meaningful risk differences between change types, domains, modules, integrations, or operational surfaces.

Confidence gates are pre-implementation guidance only. They do not replace source-code verification, test execution, or evidence-based repository inspection. Their purpose is to reduce blind discovery and guide targeted inspection before coding.

Use this exact structure:

```md
# Confidence Gates

## Purpose

## Confidence Scale

## Change Type Confidence Matrix

## Required Pre-Implementation Checks

## High-Risk Change Gates

## Files to Inspect by Change Type

## Approval Gate Recommendations

## Notes for Future Agents
```

The `Change Type Confidence Matrix` must remain language/framework/runtime agnostic and include, at minimum, these generic change categories:
- Standard feature change
- Bug fix
- Refactor
- Data model or persistence change
- Authentication/authorization change
- External integration change
- Public API or interface contract change
- Background job / queue / scheduled task change
- Configuration or environment change
- Testing-only change
- Deployment/release change
- Security-sensitive change

For each change type, include:
- Confidence level: `High`, `Medium`, `Low`, or `Unconfirmed`
- Why
- Required files or areas to inspect
- Required tests/checks
- Approval gate recommendation

Refresh `confidence-gates.md` when new risk areas, integrations, architectural changes, testing gaps, operational concerns, or domain boundaries are discovered.

## Usage Example
Run `.ai/workflows/build-project-intelligence.md` and generate `.ai/context/project-intelligence.md` for this repository. Infer architecture and conventions from repository evidence and mark uncertain findings as `Unconfirmed`.

## Maintenance Recommendation
Regenerate or refresh intelligence files after:
- major architectural changes,
- major dependency changes,
- major domain changes,
- major integration changes,
- significant refactors.

## Workflow Deliverables
- `.ai/context/project-intelligence.md`
- Optional specialized artifacts (when justified):
  - `.ai/context/architecture.md`
  - `.ai/context/domain-model.md`
  - `.ai/context/coding-patterns.md`
  - `.ai/context/integrations.md`
  - `.ai/context/testing-strategy.md`
  - `.ai/context/technical-debt.md`
  - `.ai/context/confidence-gates.md`
- Evidence-backed repository intelligence suitable for future AI sessions across Codex, Claude Code, Cursor, Roo Code, Cline, and future runtimes.
