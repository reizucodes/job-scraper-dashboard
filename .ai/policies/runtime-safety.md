# Runtime Safety Policy

## Purpose
Define operational safety boundaries for AI-assisted development work and prevent destructive or irreversible actions without control.

## Allowed Actions (No Approval Required)
- Read files and inspect diffs.
- Search code and dependencies.
- Analyze architecture and propose plans.
- Generate or modify code and documentation.
- Run tests and linters.
- Perform code review and static analysis.
- Prepare migration/deployment plans (without executing production changes).

## Approval Required Actions (Level 1)
The agent must request approval before execution:
- `git add`, `git commit`, `git merge`, `git rebase`.
- Migration execution against non-local/shared environments.
- Package installation, dependency upgrades/removals.
- File deletion or bulk file renames.
- Environment/configuration modifications.
- Deployment preparation steps that alter release state.

### Approval Request Template
```text
Action: <command or operation>
Reason: <why this is required>
Impact: <files/systems affected>
Rollback: <how to revert safely>
Approval Needed: Yes (Level 1)
```

## Explicit User Command Required (Level 2)
Never perform automatically. Only execute on direct, explicit user command:
- Production deployment execution.
- Force push operations.
- Branch deletion.
- `git reset --hard`, `git clean -fd`.
- Database destruction/reset on non-local environments.
- Production data deletion.
- Secret rotation or credential removal.
- Infrastructure destruction/irreversible changes.

### Explicit Instruction Template
```text
Requested Level 2 Action: <operation>
Target Environment: <env>
Risk: <high-level impact>
Confirmation Required: Please explicitly confirm this exact action.
```

## Runtime Safety Rules
1. If risk is unclear, pause and request clarification.
2. Prefer reversible operations and document rollback path first.
3. Record approval context in workflow artifacts.
4. Escalate high/critical risk actions to architect + devops + code-review.
5. If action-level classification is ambiguous, use `.ai/policies/approval-levels.md` as the source of truth.
