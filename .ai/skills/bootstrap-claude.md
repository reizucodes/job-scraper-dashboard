# Bootstrap Claude Skill

## Purpose
Claude bootstrap support exists to let Claude Code consume this repository's agent framework without forking framework logic.

This repository stores the reusable bootstrap skill only; it does not serve as the default Claude runtime target project.

`AGENTS.md` remains authoritative because it defines global runtime instructions, governance expectations, and response structure for all agents and workflows.

Claude-specific files must remain minimal adapters so runtime onboarding does not create competing sources of truth.

## Inputs
Required inputs for bootstrap generation:
- Repository root
- `AGENTS.md`
- `INDEX.md`
- `.ai/agents/*`
- `.ai/workflows/*`
- `.ai/policies/*`
- `.ai/templates/*`

## Expected Output
Generated artifacts:
- `CLAUDE.md` (required in the target/consumer repository)
- `.claude/` (optional, only when runtime compatibility requirements are confirmed)

## Generation Rules
- `AGENTS.md` is the authoritative runtime instruction source.
- `INDEX.md` is the runtime discovery and routing entrypoint.
- `.ai/agents/*` remain canonical.
- `.ai/workflows/*` remain canonical.
- `.ai/policies/*` remain canonical.
- `.ai/templates/*` remain canonical.
- Generated Claude files must not duplicate governance.
- Generated Claude files must not duplicate workflows.
- Generated Claude files must not duplicate agent definitions.
- Generated Claude files must not become alternate sources of truth.
- Claude adapter artifacts should primarily route execution to canonical files.
- `CLAUDE.md` is generated for consuming repositories, not committed by default to this source repository.
- Do not commit `CLAUDE.md` to `ai-agents/` unless this repository is intentionally being used as an actual Claude Code target project.
- Generated Claude files are runtime adapters only and never replace canonical framework sources.

## Example CLAUDE.md
Minimal bootstrap example:

```md
# Claude Bootstrap

1. Read `AGENTS.md` first.
2. Read `INDEX.md` second.
3. Use `.ai/agents/*`, `.ai/workflows/*`, `.ai/policies/*`, and `.ai/templates/*` for implementation guidance.

If any instruction conflicts with `AGENTS.md`, `AGENTS.md` takes precedence.
```

## Subagent Compatibility Notes
When integrating `.ai/agents/*` with Claude subagents, validate runtime-specific requirements before linking directly:
- Claude subagent runtime may require YAML frontmatter.
- A required `name` field may be enforced.
- A required `description` field may be enforced.
- Metadata format may require strict key/value frontmatter instead of markdown headings.
- File naming may need runtime-specific naming constraints.
- Directory placement may need `.claude/agents/` for discovery.

If canonical files do not satisfy these requirements exactly, use thin wrappers under `.claude/agents/`.

## Symlink Guidance
Symlinks are safe when all conditions are true:
- Canonical agent files are directly compatible with Claude subagent parser requirements.
- Target environment preserves symlinks in local development and CI.
- Repository consumers are expected to use filesystems and tooling with stable symlink support.

Symlinks are unsafe when any condition is true:
- Claude requires frontmatter or metadata not present in canonical files.
- Cross-platform tooling may break symlink resolution (packaging, archives, or constrained environments).
- Runtime discovery requires physical files in `.claude/agents/` with runtime-specific metadata.

Use wrapper files instead of symlinks when compatibility is incomplete. Wrappers must include only runtime-required metadata and a delegation reference to canonical `.ai/agents/*` instructions.
