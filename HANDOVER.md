# Handover

## Milestone

**Phase 1 — Repository Bootstrap**

Status: implementation complete on `phase-1/repository-bootstrap`; local pytest passed, while the unavailable local toolchain and PostgreSQL/Docker checks remain for GitHub Actions.

## Summary

The repository now contains a Python 3.12 modular-monolith foundation with FastAPI, typed settings, sanitized UTC JSON logging, lazy SQLAlchemy/Psycopg database ownership, Alembic, health endpoints, Docker Compose, tests, and GitHub Actions.

## Files created

- `AGENTS.md`, `ARCHITECTURE.md`, `HANDOVER.md`: agent, architecture, and milestone records.
- `pyproject.toml`, `.env.example`, `.gitignore`, `.dockerignore`: project, configuration, and security baseline.
- `Dockerfile`, `compose.yaml`: non-root API and local PostgreSQL services.
- `alembic.ini`, `alembic/`: schema migration baseline.
- `src/ev_scanner/`: API, core, and database packages.
- `tests/`: configuration, app, health, and logging tests.
- `.github/workflows/ci.yml`: Python 3.12 quality and PostgreSQL migration checks.

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

`EV_ENVIRONMENT`, `EV_APPLICATION_NAME`, `EV_LOG_LEVEL`, `EV_HOST`, `EV_PORT`, `EV_DATABASE_URL`, and `EV_PRESENTATION_TIMEZONE`. Compose additionally consumes local database bootstrap variables documented in `.env.example`.

## Migration status

Revision `0001_bootstrap` is the baseline and intentionally creates no domain tables. CI is configured to run `alembic upgrade head` against clean PostgreSQL.

## Verification results

Executed locally on 2026-07-24:

- `pytest`: **9 passed in 0.05s**. The available sandbox interpreter was Python 3.13.5, so Python 3.12 remains CI-verified rather than locally verified.
- `python -m compileall -q src tests alembic`: passed.
- `ruff check .`: not run successfully because `ruff` is not installed and the sandbox package index could not provide it.
- `ruff format --check .`: not run successfully for the same reason.
- `mypy src tests`: not run successfully because `mypy` is not installed.
- `alembic upgrade head`: attempted but could not start because the sandbox lacks Psycopg and a PostgreSQL service.
- Docker Compose smoke test: not run because Docker is not installed in the sandbox.

GitHub Actions is configured to run all required Python 3.12, Ruff, mypy, pytest, PostgreSQL, and Alembic checks on the pull request.

## Important decisions

- Modular monolith and synchronous SQLAlchemy.
- Standard-library structured logging.
- Lazy infrastructure access and replaceable readiness checks.
- Alembic only; no `create_all`.
- No provider or racing placeholders before canonical-domain design.

## Assumptions

- PostgreSQL is the long-term local database.
- Australian thoroughbred racing is the initial product domain.
- Data licensing and provider access will be researched before integration.

## Known issues and technical debt

- No real domain schema exists yet.
- No production observability or deployment target exists.
- Basic regex redaction is defensive, not a substitute for never logging secrets.
- Dependency lock-file strategy can be selected once local developer tooling is confirmed.

## External dependencies

Runtime dependencies are FastAPI, Pydantic, pydantic-settings, SQLAlchemy, Psycopg, Alembic, and Uvicorn. PostgreSQL is the only required service.

## Explicitly deferred

Racing-domain entities, providers, scraping, odds/EV mathematics, entity matching, historical ingestion, workers, Redis, frontend, paper trading, backtesting, modelling, explanations, and betting execution.

## Exact next milestone

**Phase 2 — Canonical racing domain and provenance models**

Define typed and persisted meeting, race, runner, horse, jockey, trainer, track, result, price-quote, source, and provenance concepts with migrations and deterministic tests. Do not add live providers, scraping, or EV calculations in that milestone.
