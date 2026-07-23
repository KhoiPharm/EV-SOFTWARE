# Handover

## Milestone

**Phase 1 — Repository Bootstrap**

Status: complete on `phase-1/repository-bootstrap`. Pull request CI run 11 passed all quality, migration, and Docker Compose smoke checks.

## Summary

The repository now contains a Python 3.12 modular-monolith foundation with FastAPI, typed settings, sanitized UTC JSON logging, lazy SQLAlchemy/Psycopg database ownership, Alembic, health endpoints, Docker Compose, deterministic tests, and GitHub Actions.

## Files created

- `AGENTS.md`, `ARCHITECTURE.md`, `HANDOVER.md`: agent, architecture, and milestone records.
- `pyproject.toml`, `.env.example`, `.gitignore`, `.dockerignore`: project, configuration, and security baseline.
- `Dockerfile`, `compose.yaml`: non-root API and local PostgreSQL services.
- `alembic.ini`, `alembic/`: schema migration baseline.
- `src/ev_scanner/`: API, core, and database packages.
- `tests/`: configuration, app, health, and logging tests.
- `.github/workflows/ci.yml`: Python 3.12 quality, migration, and Compose smoke checks.

## Files modified

- `README.md`: replaced the placeholder with accurate setup, usage, limitations, and responsible-use documentation.

## Current architecture

One local FastAPI modular monolith. Configuration and logging are application-wide boundaries. Database engine/session factories are lazy. Alembic owns schema changes. There are no racing domains or providers.

## Public interfaces

- `ev_scanner.api.app.create_app(settings=None) -> FastAPI`
- `ev_scanner.api.app:app`
- `GET /health/live`
- `GET /health/ready`
- `ev_scanner.core.config.Settings`
- `ev_scanner.core.config.get_settings()`
- `ev_scanner.db.engine.get_engine()`
- `ev_scanner.db.session.get_session()`

## Configuration variables

`EV_ENVIRONMENT`, `EV_APPLICATION_NAME`, `EV_LOG_LEVEL`, `EV_HOST`, `EV_PORT`, `EV_DATABASE_URL`, and `EV_PRESENTATION_TIMEZONE`. Compose additionally consumes the local database bootstrap variables documented in `.env.example`.

## Migration status

Revision `0001_bootstrap` is the baseline and intentionally creates no domain tables. `alembic upgrade head` passed against clean PostgreSQL 17 in GitHub Actions.

## Verification results

Executed locally on 2026-07-24:

- `pytest`: **9 passed in 0.05s** using the available Python 3.13.5 sandbox interpreter.
- `python -m compileall -q src tests alembic`: passed.
- Ruff, mypy, PostgreSQL, and Docker were unavailable in the local sandbox; the attempted local migration also lacked Psycopg.

Verified in GitHub Actions run 11 using Python 3.12:

- `ruff check .`: passed.
- `ruff format --check .`: passed.
- `mypy src tests`: passed.
- `pytest`: passed.
- `alembic upgrade head`: passed against clean PostgreSQL 17.
- Docker Compose smoke test: built the non-root API image, started PostgreSQL and the API, applied migrations, and received a successful response from `GET /health/ready`.

## Important decisions

- Modular monolith and synchronous SQLAlchemy.
- Standard-library structured logging.
- Lazy infrastructure access and replaceable readiness checks.
- Alembic only; no `create_all`.
- No provider or racing placeholders before canonical-domain design.
- Separate CI jobs for code quality, migration validation, and full Compose startup.

## Assumptions

- PostgreSQL is the long-term local database.
- Australian thoroughbred racing is the initial product domain.
- Data licensing and provider access will be researched before integration.

## Known issues and technical debt

- No real domain schema exists yet.
- No production observability or deployment target exists.
- Basic regex redaction is defensive, not a substitute for never logging secrets.
- A dependency lock-file strategy remains to be selected once local developer tooling is confirmed.

## External dependencies

Runtime dependencies are FastAPI, Pydantic, pydantic-settings, SQLAlchemy, Psycopg, Alembic, and Uvicorn. PostgreSQL is the only required service.

## Explicitly deferred

Racing-domain entities, providers, scraping, odds/EV mathematics, entity matching, historical ingestion, workers, Redis, frontend, paper trading, backtesting, modelling, explanations, and betting execution.

## Exact next milestone

**Phase 2 — Canonical racing domain and provenance models**

Define typed and persisted meeting, race, runner, horse, jockey, trainer, track, result, price-quote, source, and provenance concepts with migrations and deterministic tests. Do not add live providers, scraping, or EV calculations in that milestone.
