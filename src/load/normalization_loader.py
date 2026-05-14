"""Load and execute SQL files that define and seed the normalized schema."""

import logging
from pathlib import Path
from time import perf_counter

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)

SQL_DIR = Path(__file__).resolve().parent / "sql"


class NormalizationExecutionError(Exception):
    """Raised when reading or executing normalization SQL fails."""


def read_sql_file(file_name: str) -> str:
    """Read a UTF-8 SQL file from ``src/load/sql``.

    Args:
        file_name: File name only (e.g. ``normalized_schema.sql``).

    Returns:
        Full file contents.

    Raises:
        NormalizationExecutionError: If the file is missing or cannot be read.
    """
    sql_file_path = SQL_DIR / file_name

    logger.info("Reading normalization SQL file '%s'", sql_file_path)

    try:
        return sql_file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        logger.exception("Normalization SQL file not found: '%s'", sql_file_path)
        raise NormalizationExecutionError(
            f"Normalization SQL file not found: '{sql_file_path}'"
        ) from exc
    except OSError as exc:
        logger.exception("Failed to read normalization SQL file: '%s'", sql_file_path)
        raise NormalizationExecutionError(
            f"Failed to read normalization SQL file: '{sql_file_path}'"
        ) from exc


def execute_sql_script(sql_script: str, *, step_name: str) -> None:
    """Run a SQL script as one or more statements inside a single transaction.

    Statements are split on semicolons (see ``split_sql_statements``). Each
    fragment is executed in order using ``engine.begin()`` so the step commits
    or rolls back atomically.

    Args:
        sql_script: Full SQL text, typically from ``read_sql_file``.
        step_name: Logical name for logging and error messages.

    Raises:
        ValueError: If ``sql_script`` is empty or yields no executable statements.
        NormalizationExecutionError: On SQLAlchemy execution errors.
    """
    if not sql_script.strip():
        raise ValueError(f"SQL script for step '{step_name}' cannot be empty")

    statements = split_sql_statements(sql_script)

    if not statements:
        raise ValueError(
            f"SQL script for step '{step_name}' does not contain executable statements"
        )

    logger.info(
        "Starting normalization step '%s' with %d SQL statements",
        step_name,
        len(statements),
    )

    engine = create_postgres_engine()

    try:
        with engine.begin() as connection:
            for index, statement in enumerate(statements, start=1):
                statement_preview = shorten_sql_for_log(statement)
                start_time = perf_counter()

                logger.info(
                    "Executing normalization step '%s' statement %d/%d: %s",
                    step_name,
                    index,
                    len(statements),
                    statement_preview,
                )

                connection.execute(text(statement))

                elapsed = perf_counter() - start_time
                logger.info(
                    (
                        "Finished normalization step '%s' statement %d/%d "
                        "in %.2f seconds"
                    ),
                    step_name,
                    index,
                    len(statements),
                    elapsed,
                )

        logger.info("Finished normalization step '%s'", step_name)

    except SQLAlchemyError as exc:
        logger.exception("Normalization step '%s' failed", step_name)
        raise NormalizationExecutionError(
            f"Failed to execute normalization step '{step_name}'"
        ) from exc


def create_normalized_schema() -> None:
    """Create normalized tables and indexes from ``normalized_schema.sql``."""
    logger.info("Normalized schema creation step started")

    sql_script = read_sql_file("normalized_schema.sql")
    execute_sql_script(sql_script, step_name="create_normalized_schema")

    logger.info("Normalized schema creation step finished")


def seed_reference_entities() -> None:
    """Seed lookup tables (companies, platforms, job titles, etc.) from raw jobs."""
    logger.info("Reference entities seed step started")

    sql_script = read_sql_file("normalized_seed_reference_entities.sql")
    execute_sql_script(sql_script, step_name="seed_reference_entities")

    logger.info("Reference entities seed step finished")


def split_sql_statements(sql_script: str) -> list[str]:
    """Split ``sql_script`` on ``;`` into non-empty, semicolon-terminated fragments.

    Note:
        Semicolons inside string literals are not handled; keep scripts simple or
        avoid embedded semicolons in strings.

    Args:
        sql_script: Full SQL file contents.

    Returns:
        List of SQL strings, each ending with ``;``.
    """
    statements = [
        statement.strip() for statement in sql_script.split(";") if statement.strip()
    ]
    return [f"{statement};" for statement in statements]


def shorten_sql_for_log(sql_statement: str, max_length: int = 160) -> str:
    """Collapse whitespace and truncate ``sql_statement`` for safe log lines."""
    single_line = " ".join(sql_statement.split())
    if len(single_line) <= max_length:
        return single_line
    return f"{single_line[:max_length]}..."


def _run_seed_step(*, sql_file_name: str, step_name: str, log_label: str) -> None:
    """Load ``sql_file_name`` and execute it, wrapping failures consistently.

    Raises:
        NormalizationExecutionError: On read, validation, or SQL execution errors.
    """
    logger.info("%s step started", log_label)

    try:
        sql_script = read_sql_file(sql_file_name)
        execute_sql_script(sql_script, step_name=step_name)
    except (OSError, SQLAlchemyError, ValueError) as exc:
        logger.exception("%s step failed", log_label)
        raise NormalizationExecutionError(
            f"Failed to execute normalization step '{step_name}'"
        ) from exc

    logger.info("%s step finished", log_label)


def seed_locations() -> None:
    """Populate normalized location rows from distinct raw job locations."""
    _run_seed_step(
        sql_file_name="normalized_seed_locations.sql",
        step_name="seed_locations",
        log_label="Locations seed",
    )


def seed_skills() -> None:
    """Insert skills and types derived from raw ``job_skills`` / ``job_type_skills``."""
    _run_seed_step(
        sql_file_name="normalized_seed_skills.sql",
        step_name="seed_skills",
        log_label="Skills seed",
    )


def seed_jobs() -> None:
    """Insert normalized ``jobs`` rows joined to reference and location tables."""
    _run_seed_step(
        sql_file_name="normalized_seed_jobs.sql",
        step_name="seed_jobs",
        log_label="Jobs seed",
    )


def seed_job_skills() -> None:
    """Populate ``job_skills`` links from raw JSON skill arrays and ``skills``."""
    _run_seed_step(
        sql_file_name="normalized_seed_job_skills.sql",
        step_name="seed_job_skills",
        log_label="Job skills seed",
    )
