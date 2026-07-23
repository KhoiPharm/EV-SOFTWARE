# AGENTS.md

## Purpose

EV-SOFTWARE is a locally hosted Australian thoroughbred racing decision-support and expected-value analysis platform. It must never claim guaranteed profit or certainty.

## Read first

Before changing code, read `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, and `HANDOVER.md`. Inspect the current tree and preserve legitimate existing work.

## Supported environment

- Python 3.12 only for the current baseline.
- Modular monolith under `src/ev_scanner`.
- PostgreSQL schema changes are managed only by Alembic.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
mypy src tests
alembic upgrade head
docker compose up --build
```

## Module boundaries

- `api`: application composition, HTTP routes, and transport schemas.
- `core`: canonical settings, logging, and application-wide errors.
- `db`: SQLAlchemy base, engine, sessions, health, and migration ownership.
- Future racing domains, provider adapters, calculations, and models must live outside route handlers.
- Keep route handlers thin and dependencies replaceable.
- Avoid global mutable state and import-time network or database activity.

## Provider and data-access rules

- Do not scrape or integrate a provider without documented permission, terms review, and an approved milestone.
- Never bypass authentication, anti-bot controls, paywalls, geographic restrictions, or rate limits.
- Raw provider dictionaries must not escape adapter boundaries.
- Provider identifiers are scoped to that provider and are not globally unique.
- Internal identifiers and normalized display names are distinct concepts.

## Data rules

- Use `Decimal`, never binary floating point, for future money, odds, stakes, financially relevant probabilities, and EV calculations. Document precision and rounding.
- All system timestamps are timezone-aware and stored in UTC. `Australia/Sydney` is only the default presentation timezone.
- Future ingested data must retain provider, provider-scoped ID, source timestamp, ingestion timestamp, immutable source reference, adapter/schema version, transformation lineage, and data-quality status.

## Security

- Never commit `.env`, tokens, cookies, credentials, certificates, account identifiers, or private keys.
- Never log secrets, complete database URLs, or complete provider payloads.
- Do not add unrestricted debug/configuration endpoints, hidden telemetry, or analytics.

## Testing

- Tests must be deterministic, isolated, and require no internet, paid data, racing account, or real credential.
- Use fixtures and dependency overrides at boundaries.
- Do not weaken linting or typing globally to make checks pass.
- Add tests for successful and failed behaviour, sanitization, and time/data edge cases relevant to each milestone.

## Documentation

- Update `HANDOVER.md` after every milestone using actual results.
- Update `README.md` and `ARCHITECTURE.md` whenever user-facing setup or architecture changes.
- Update this file whenever agent rules or commands change.

## Definition of done

A milestone is done only when its acceptance criteria are implemented, tests are added, all configured quality commands have been run, documentation matches reality, secrets are absent, the diff is reviewed, and work is committed on the requested feature branch.

## Completion report

Report summary, created/modified files, public interfaces, tests and exact results, assumptions, known limitations, remaining work, Git status, commit/PR information, and explicit confirmation that out-of-scope items were not implemented.
