# Skills (Future Extension Point)

## Purpose
Skills are reusable knowledge modules that can be shared across multiple agents, workflows, and technology stacks.

Skills:
- capture repeatable implementation guidance,
- reduce duplicated documentation,
- improve consistency across stacks.

Skills do **not** own workflow responsibilities.  
Skills do **not** replace agents.

## Example Future Skills (Examples Only)
- `api-design.md`
- `api-security.md`
- `testing.md`
- `openapi.md`
- `database-design.md`
- `performance.md`
- `observability.md`

These are examples only and should not be created prematurely.

## When To Create A Skill
Create a skill when:
- the same guidance appears across three or more agents,
- multiple technology stacks share the same implementation guidance,
- documentation duplication becomes difficult to maintain,
- shared engineering standards emerge.

Practical examples:
- The same OpenAPI contract guidance appears in Laravel, FastAPI, and Node Express agents.
- The same test-coverage strategy is repeated across frontend and backend agents.

## When NOT To Create A Skill
Do not create a skill:
- for one-time project requirements,
- for speculative future needs,
- for guidance only referenced by a single agent,
- simply because a topic might become useful later.

Avoid premature abstraction.

## Relationship To Agents
Agents may reference skills when shared guidance is extracted.

Examples:
- Security Agent -> `api-security` skill
- Laravel Agent -> `testing` skill, `openapi` skill
- FastAPI Agent -> `api-design` skill, `api-security` skill

## Rule Of Thumb
If the same guidance appears in three or more locations, consider extracting it into a skill.  
Otherwise keep the guidance where it currently belongs.

