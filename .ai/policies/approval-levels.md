# Approval Levels Policy

## Purpose
Standardize approval controls so all agents apply the same execution boundaries.

## Level 0 (Safe Automated Actions)
No explicit approval required.

Examples:
- Read files and search files.
- Analyze code and architecture.
- Generate documentation.
- Generate code and non-destructive edits.
- Run tests and linters.
- Review code.

## Level 1 (Approval Required)
Agent must request approval before execution.

Examples:
- `git add`
- `git commit`
- `git merge`
- `git rebase`
- `git stash`
- `git restore`
- `git checkout` existing branch
- `git switch` existing branch
- `git cherry-pick`
- `git revert`
- `git tag` (create)
- create branch
- dependency installation/removal/upgrades
- migration execution
- file deletion
- environment configuration changes

## Level 2 (Explicit User Instruction Only)
Must not run unless the user explicitly requests the exact action.

Examples:
- `git push`
- `git push --force`
- `git reset`
- `git reset --hard`
- `git clean`
- `git clean -fd`
- branch deletion
- tag deletion
- production deployment
- production migrations
- credential deletion
- secret rotation
- infrastructure destruction
- `DROP TABLE`
- `DROP DATABASE`
- `TRUNCATE TABLE`

## Decision Matrix
| Action Type | Level | Who Approves | Agent Behavior |
|---|---|---|---|
| Analysis, docs, tests, planning | 0 | Not required | Execute directly |
| State-changing development operations | 1 | User approval | Request approval before running |
| Irreversible/destructive/prod-critical actions | 2 | Explicit user command | Do not initiate; require explicit instruction |

## Examples
- Run unit tests: Level 0.
- Install new package: Level 1.
- Create a git tag: Level 1.
- Push to remote: Level 2.
- `git reset --hard`: Level 2.

## Approval Request Examples
```text
Action: git cherry-pick <commit>
Reason: Apply approved fix from mainline to current branch.
Impact: Updates tracked files in current branch.
Rollback: git revert <new-commit> if required.
Approval Needed: Yes (Level 1)
```

```text
Action: Run migration in shared staging environment
Reason: Validate schema compatibility before release.
Impact: Alters staging database schema.
Rollback: Use documented down migration.
Approval Needed: Yes (Level 1)
```

## Level 2 Rationale
Level 2 operations can be irreversible, affect shared history, or impact production data/availability. These actions require explicit user instruction to prevent accidental damage.
