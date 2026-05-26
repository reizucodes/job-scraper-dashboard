# Task Template

Use this template for small, routine engineering work items that can be scoped and delivered quickly.

## Template
```text
Title:

Type: Feature | Bugfix | Refactor | Maintenance

Context:

Requirements:
- 

Acceptance Criteria:
- 

Out of Scope:
- 

Risks: (optional)
- 

Notes:
- 
```

## Usage Guidance
Use `task.md` when work is straightforward and can be completed without deep discovery.

Use `feature-spec.md` instead when the change introduces a new business capability, new subsystem, new payment/authentication flow, cross-team coordination, or significant architecture risk.

Agents should consume `task.md` as the working contract for day-to-day execution:
- `architect` and `security` validate only where risk warrants.
- stack agent implements against the listed requirements.
- `qa` validates acceptance criteria and edge behavior.

### Good Task Candidates
- Add pagination
- Add sorting
- Fix validation bug
- Add endpoint
- Update UI behavior
- Improve error messages

### Use Feature Spec Instead
- New business capability
- New subsystem
- New payment flow
- New authentication flow
- Multi-team initiative
- Major architecture change

## Example (Completed)
```text
Title: Add Pagination to Project Members API

Type: Feature

Context:
The project members endpoint returns full lists and causes slow responses on large projects.

Requirements:
- Add `page` and `per_page` query params to `GET /api/v1/projects/{id}/members`.
- Default `per_page` to 25, maximum 100.
- Return pagination metadata in response.

Acceptance Criteria:
- Endpoint returns paginated results with stable ordering.
- Invalid `per_page` values return validation errors.
- Existing clients without pagination params continue to work.

Out of Scope:
- Frontend pagination UI changes.
- Role/permission model changes.

Risks:
- Existing consumers may assume full result set in one call.

Notes:
- Add OpenAPI response example with pagination metadata.
- Add feature tests for default, custom, and invalid pagination params.
```

