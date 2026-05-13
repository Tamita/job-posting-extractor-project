import logging
from time import perf_counter
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)

SQL_DIR = Path(__file__).resolve().parent / "sql"


class NormalizationExecutionError(Exception):
    """Raised when normalization SQL execution fails."""


def read_sql_file(file_name: str) -> str:
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
    logger.info("Normalized schema creation step started")

    sql_script = read_sql_file("normalized_schema.sql")
    execute_sql_script(sql_script, step_name="create_normalized_schema")

    logger.info("Normalized schema creation step finished")


def seed_reference_entities() -> None:
    logger.info("Reference entities seed step started")

    sql_script = read_sql_file("normalized_seed_reference_entities.sql")
    execute_sql_script(sql_script, step_name="seed_reference_entities")

    logger.info("Reference entities seed step finished")


def split_sql_statements(sql_script: str) -> list[str]:
    statements = [
        statement.strip() for statement in sql_script.split(";") if statement.strip()
    ]
    return [f"{statement};" for statement in statements]


def shorten_sql_for_log(sql_statement: str, max_length: int = 160) -> str:
    single_line = " ".join(sql_statement.split())
    if len(single_line) <= max_length:
        return single_line
    return f"{single_line[:max_length]}..."


def _run_seed_step(*, sql_file_name: str, step_name: str, log_label: str) -> None:
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
    _run_seed_step(
        sql_file_name="normalized_seed_locations.sql",
        step_name="seed_locations",
        log_label="Locations seed",
    )


def seed_skills() -> None:
    _run_seed_step(
        sql_file_name="normalized_seed_skills.sql",
        step_name="seed_skills",
        log_label="Skills seed",
    )
