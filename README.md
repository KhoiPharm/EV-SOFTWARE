# EV-SOFTWARE

Locally hosted Australian thoroughbred horse-racing decision-support and expected-value analysis platform.

> This software is for analysis and research. It does not guarantee profit, predict outcomes with certainty, or place bets automatically. Gambling involves financial risk.

## Current capabilities

- Python 3.12 FastAPI application factory.
- Typed environment configuration.
- UTC structured JSON logging with basic secret redaction.
- Lazy SQLAlchemy 2 and Psycopg 3 database foundation.
- Alembic migration baseline.
- Liveness and PostgreSQL-backed readiness endpoints.
- Docker Compose for the API and PostgreSQL.
- Offline unit tests and GitHub Actions baseline checks.

## Not implemented

No racing data models, form data, Betfair, bookmaker feeds, scraping, odds calculations, EV calculations, frontend, modelling, paper trading, or automatic betting currently exists.

## Prerequisites

- Python 3.12
- PostgreSQL 17 or Docker with Docker Compose

## Local setup without Docker

```bash
git clone https://github.com/KhoiPharm/EV-SOFTWARE.git
cd EV-SOFTWARE
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

Create the local database identified by `EV_DATABASE_URL`, then run:

```bash
alembic upgrade head
uvicorn ev_scanner.api.app:app --reload --host 127.0.0.1 --port 8000
```

Environment precedence is explicit constructor arguments, operating-system environment variables, `.env`, then safe development defaults.

## Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The API is available on `http://127.0.0.1:8000`. PostgreSQL is published only on localhost by default. The API waits for PostgreSQL, applies Alembic migrations, and then starts.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `EV_ENVIRONMENT` | `development` | `development`, `test`, or `production` |
| `EV_APPLICATION_NAME` | `EV Scanner` | API title |
| `EV_LOG_LEVEL` | `INFO` | Structured-log threshold |
| `EV_HOST` | `127.0.0.1` | Local bind host |
| `EV_PORT` | `8000` | Local bind port |
| `EV_DATABASE_URL` | local PostgreSQL placeholder | SQLAlchemy/Psycopg URL; treated as secret |
| `EV_PRESENTATION_TIMEZONE` | `Australia/Sydney` | IANA presentation timezone; storage remains UTC |

Compose also reads `EV_DB_USER`, `EV_DB_PASSWORD`, `EV_DB_NAME`, and `EV_DB_PORT` to bootstrap its local database container.

Never commit `.env` or real credentials.

## Endpoints

```bash
curl http://127.0.0.1:8000/health/live
curl http://127.0.0.1:8000/health/ready
```

`/health/live` does not touch the database. `/health/ready` returns HTTP 503 with a sanitized response if PostgreSQL is unavailable.

## Migrations

```bash
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "describe change"
```

Inspect every generated migration before committing it. Do not use `Base.metadata.create_all` for application schema management.

## Tests and quality

```bash
pytest
ruff check .
ruff format --check .
mypy src tests
```

Tests require no internet, provider account, paid racing data, or real credentials.

## Repository structure

```text
src/ev_scanner/api/   FastAPI composition, routes, schemas
src/ev_scanner/core/  Settings, errors, logging
src/ev_scanner/db/    SQLAlchemy, readiness, sessions
tests/                Deterministic tests
alembic/              Versioned database migrations
```

## Troubleshooting

- Readiness returns 503: confirm PostgreSQL is running and `EV_DATABASE_URL` is correct.
- Invalid timezone: use an IANA name such as `Australia/Sydney`.
- Port collision: change the localhost port mapping or `EV_PORT` for non-Compose local runs.
- Compose state problems: `docker compose down` preserves the named database volume; add `-v` only when intentionally deleting local data.

## Known limitations

This is only the repository bootstrap. It has no racing data and cannot identify an opportunity. The next milestone is **Phase 2 — Canonical racing domain and provenance models**.
