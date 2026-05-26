# Threat Model Template

Use this template for focused security analysis of APIs, web apps, and internal tools.

## Template
```text
System Overview:

Assets:
- 

Entry Points:
- 

Trust Boundaries:
- 

Threat Categories:
Authentication:
- 

Authorization:
- 

Input Validation:
- 

File Uploads:
- 

Secrets Exposure:
- 

Dependency Risks:
- 

Rate Limiting:
- 

Denial of Service:
- 

Data Leakage:
- 

Logging Risks:
- 

Mitigations:
- 

Residual Risks:
- 

Risk Classification: Low | Medium | High | Critical

Security Review Outcome: Approved | Approved With Conditions | Rejected

Reviewer Notes:
- 
```

## Usage Guidance
Threat modeling is recommended when:
- authentication exists,
- authorization exists,
- sensitive information exists,
- public APIs exist,
- file uploads exist,
- payment processing exists,
- risk classification is Medium or higher.

Threat modeling may be unnecessary for low-risk, isolated changes with no auth/data boundary impact.

How `security` should use this template:
- identify realistic threat paths,
- map concrete mitigations to each material threat,
- classify residual risk and define release conditions.

Workflow fit:
- typically between `architect` and implementation for feature work,
- during bugfix/release when security-sensitive surfaces are affected.

## Example (Completed): JWT-based User Authentication API
```text
System Overview:
Public API providing login, token refresh, and authenticated profile access using JWT access tokens.

Assets:
- User accounts
- Password hashes
- JWT signing key
- Access tokens
- Administrative functions

Entry Points:
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- GET /api/v1/me
- Admin-only endpoints

Trust Boundaries:
- Public internet to API gateway
- API app to database
- API app to secret store

Threat Categories:
Authentication:
- Credential stuffing against login endpoint.

Authorization:
- Token with missing/incorrect role claims accessing admin routes.

Input Validation:
- Malformed JSON and oversized payloads on login/refresh.

File Uploads:
- Not applicable for this service.

Secrets Exposure:
- JWT signing key accidentally logged or exposed in debug output.

Dependency Risks:
- Auth library vulnerability in JWT verification package.

Rate Limiting:
- Brute-force attempts without throttling.

Denial of Service:
- High request volume on refresh endpoint.

Data Leakage:
- Detailed auth error responses exposing account existence.

Logging Risks:
- Logs containing raw Authorization headers.

Mitigations:
- Rate limiting + IP/user throttling on auth endpoints.
- Role/scope checks on privileged routes.
- Strict payload validation and request size limits.
- JWT key stored in secret manager, never logged.
- Dependency scanning and patch policy for auth packages.
- Generic auth failure messages.
- Redaction of auth headers in logs.

Residual Risks:
- Automated credential attacks still possible at low volume.
- Token theft risk remains if client storage is compromised.

Risk Classification: Medium

Security Review Outcome: Approved With Conditions

Reviewer Notes:
- Add alerting for repeated login failures.
- Add periodic key rotation runbook validation.
```

