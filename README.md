# Job posting extractor

ETL pipeline that ingests job posting CSV data, loads a raw PostgreSQL table, then creates and seeds a normalized relational schema for downstream analytics and applications.

## Requirements

- Python **3.13+** (see `pyproject.toml`)
- [Poetry](https://python-poetry.org/) for dependencies and the virtual environment
- [PostgreSQL](https://www.postgresql.org/) reachable with credentials from `.env`
- [GNU Make](https://www.gnu.org/software/make/) (optional; wraps Poetry)

## Installation

```bash
poetry install
cp .env.example .env
# Edit .env with your PostgreSQL host, database name, user, and password.
```

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_DB` | Database name | `job_postings` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | *(empty)* |
| `POSTGRES_SCHEMA` | Schema for the raw load table | `public` |
| `POSTGRES_TABLE` | Raw staging table name | `raw_jobs` |

`.env` is loaded from the **repository root** (see `src/config/settings.py`).

## Data layout

The input CSV path is `RAW_JOBS_FILE` in `src/config/settings.py` (bronze layer under the configured `DATA_DIR`). The sample file name is `data_jobs.csv`; ensure that file exists before running the pipeline.

## Pipeline overview

Order of steps in `src/main.py`:

1. **Bootstrap** — Ensure the target PostgreSQL database exists.
2. **Extract** — Read the jobs CSV into a pandas `DataFrame`.
3. **Transform** — Parse semi-structured columns (e.g. skills) and validate with Pandera.
4. **Load (raw)** — Replace the configured raw table with the validated frame (JSON types for nested columns).
5. **Normalize** — Run DDL (`normalized_schema.sql`) and seed SQL for reference entities, locations, skills, jobs, and job–skill links.

## Common commands

| Command | Description |
|---------|-------------|
| `make help` | List Makefile targets and short descriptions. |
| `make install` | Install dependencies with Poetry. |
| `make run` | Run the full pipeline (`poetry run python -m src.main`). |
| `make fix` | Apply **Black** formatting and **Ruff** auto-fixes to `src/` and `tests/` (writes files). |
| `make qa` | Quality gate: Black `--check`, Ruff, Mypy, and pytest (no formatting writes). |
| `make test` | Run pytest with verbose output. |
| `make test-cov` | Run tests with a coverage report. |

## Git branching

- `main` — primary branch  
- `develop` — integration branch  
- Branch naming: `scope/description`, for example `feature/...`, `bugfix/...`, `docs/...`, `test/...`.

## Development tooling

- **pytest** — tests  
- **ruff** — lint (`make lint`, auto-fix via `make lint-fix` / `make fix`)  
- **black** — format (`make format`, check via `make format-check` / `make qa`)  
- **mypy** — static types (`make type-check` / `make qa`)

## Project layout

```text
src/
  config/       # Environment-backed settings
  extract/      # CSV ingestion
  transform/    # Parsing and Pandera validation
  load/         # Raw load, DB bootstrap, normalization SQL runner
    sql/        # Normalized DDL and seed scripts
  utils/        # Logging and shared helpers
tests/
```
