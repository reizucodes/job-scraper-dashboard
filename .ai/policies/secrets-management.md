# Secrets Management Policy

## Purpose
Prevent accidental exposure of credentials, tokens, keys, and other sensitive configuration values.

## Never
- Commit secrets to source control.
- Print secrets in terminal output.
- Log secrets in application logs or test output.
- Expose `.env` values in docs, code snippets, or examples.
- Store credentials directly in source code.
- Return production credentials in agent responses.
- Upload secret values to external services.
- Share access tokens, API keys, or private keys.
- Include decrypted secret material in issue trackers or PR comments.

## Always
- Use environment variables or approved secret managers.
- Mask/redact sensitive values in outputs and logs.
- Treat credentials and tokens as sensitive by default.
- Rotate compromised credentials through secure channels.
- Use least privilege for generated configuration guidance.

## AI Assistant Rules
Agents must:
- Refuse requests to reveal real secrets.
- Redact sensitive values when summarizing configs/logs.
- Avoid generating fake "realistic" credentials that could be mistaken as valid.
- Warn when unsafe secret handling is detected.
- Refer to approval and runtime safety policies before risky secret operations.

## Practical Examples
- Safe:
  - `DB_PASSWORD=***REDACTED***`
  - "Store this token in your secret manager; do not commit it."
- Unsafe:
  - Posting full `.env` contents.
  - Returning private key blocks in chat.
  - Suggesting credentials be hardcoded for convenience.

