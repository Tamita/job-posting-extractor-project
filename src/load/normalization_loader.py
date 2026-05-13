import logging
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

    logger.info("Starting normalization step '%s'", step_name)

    engine = create_postgres_engine()

    try:
        with engine.begin() as connection:
            connection.execute(text(sql_script))
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
