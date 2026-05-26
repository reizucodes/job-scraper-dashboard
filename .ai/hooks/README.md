# Hooks (Future Extension Point)

## Purpose
Hooks are optional automation scripts that run before or after AI-assisted actions.

Hooks can automate repetitive validation, formatting, testing, and safety tasks.  
Hooks should only be introduced when real usage patterns justify automation.

## Example Future Hooks (Examples Only)
- `laravel-validate.sh`
- `vue-validate.sh`
- `react-validate.sh`
- `fastapi-validate.sh`
- `security-scan.sh`
- `prevent-force-push.sh`

These are examples only and should not be implemented automatically.

## Typical Use Cases

### Validation
- PHPUnit / Pest
- Vitest
- Pytest
- Type checking
- Build verification

### Formatting
- Laravel Pint
- ESLint
- Prettier
- Ruff

### Security
- Secret scanning
- Dependency scanning
- Dangerous command detection

### Safety Controls
- Prevent force push
- Restrict destructive commands
- Protect production environments

## When To Create A Hook
Create a hook when:
- a manual task is repeated frequently,
- validation steps are consistently forgotten,
- safety checks need automation,
- the trigger is deterministic and reliable.

Practical examples:
- Running the same test command before nearly every commit.
- Repeatedly forgetting lint/type checks before review.

## When NOT To Create A Hook
Do not create a hook:
- for rare actions,
- for speculative future needs,
- for tasks without a reliable trigger,
- if automation introduces more complexity than value.

Avoid premature automation.

## Rule Of Thumb
If a command is manually executed multiple times per day, consider automating it with a hook.  
Otherwise keep the process manual.

## Relationship To Policies
Policies define expectations.  
Hooks may eventually automate enforcement of those expectations.

Examples:
- Policy: run tests before completion.  
  Future hook: automatically execute validation scripts.
- Policy: protect secrets.  
  Future hook: run secret scanning tools.

