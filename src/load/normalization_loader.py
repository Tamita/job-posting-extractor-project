import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)


class NormalizationExecutionError(Exception):
    """Raised when normalization SQL execution fails."""


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
    execute_sql_script(
        """
        SELECT 1;
        """,
        step_name="create_normalized_schema",
    )
    logger.info("Normalized schema creation step finished")
