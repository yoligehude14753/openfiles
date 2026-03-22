# Security Policy

## Threat Model

OpenFiles is designed as a **local-first, single-user application**. The default configuration assumes the API server is only accessible from `localhost` or a trusted local network.

**Important:** OpenFiles does not include authentication or authorization on its API endpoints. If you expose the server to a public network (e.g., binding to `0.0.0.0` without a reverse proxy), anyone with network access can read your indexed files and modify settings.

### Recommendations for Network Deployments

- Place OpenFiles behind a reverse proxy (e.g., nginx, Caddy) with authentication if you need remote access.
- Do not expose port 8000 directly to the internet.
- Review the `CORS` settings in `src/api/app.py` — the default allows all origins for local development convenience.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue.
2. Email **security@openfiles.dev** (or open a private security advisory on GitHub).
3. Include a description of the vulnerability, steps to reproduce, and potential impact.
4. We will acknowledge receipt within 48 hours and aim to provide a fix or mitigation within 7 days.

## API Key Handling

- API keys configured via `.env` are never returned in plaintext through the settings API — they are masked (first 4 + last 4 characters shown).
- The `.env` file should not be committed to version control. It is listed in `.gitignore`.

## Data Privacy

- All file content, embeddings, and metadata are stored locally in SQLite.
- When using Ollama, no data leaves your machine.
- When using cloud LLM providers (OpenAI, OpenRouter, etc.), file summaries and search queries are sent to the provider's API. Review your provider's data retention policy.
