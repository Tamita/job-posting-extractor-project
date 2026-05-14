import logging

import pandas as pd
from sqlalchemy import JSON

from src.config.settings import POSTGRES_SCHEMA, POSTGRES_TABLE
from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)


def prepare_dataframe_for_postgres_load(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``df`` ready for bulk load into the raw staging table.

    Inserts a monotonic ``raw_job_id`` column (1..n). Coerces ``job_posted_date``
    to datetimes when that column exists.

    Args:
        df: Validated jobs dataframe.

    Returns:
        Dataframe including ``raw_job_id`` and typed dates where applicable.
    """
    prepared_df = df.copy()

    prepared_df.insert(0, "raw_job_id", range(1, len(prepared_df) + 1))

    if "job_posted_date" in prepared_df.columns:
        prepared_df["job_posted_date"] = pd.to_datetime(
            prepared_df["job_posted_date"],
            errors="coerce",
        )

    return prepared_df


def load_jobs_to_postgres(df: pd.DataFrame) -> None:
    """Replace the configured raw PostgreSQL table with ``df``.

    Uses ``if_exists='replace'`` and maps nested columns to SQLAlchemy ``JSON``
    where configured. Schema and table names come from settings.

    Args:
        df: Validated dataframe after parsing and Pandera checks.

    Raises:
        Exception: Database or pandas ``to_sql`` errors are logged and re-raised.
    """
    logger.info(
        "Starting PostgreSQL load for table '%s.%s'",
        POSTGRES_SCHEMA,
        POSTGRES_TABLE,
    )

    try:
        prepared_df = prepare_dataframe_for_postgres_load(df)
        engine = create_postgres_engine()

        prepared_df.to_sql(
            name=POSTGRES_TABLE,
            con=engine,
            schema=POSTGRES_SCHEMA,
            if_exists="replace",
            index=False,
            dtype={
                "job_skills": JSON,
                "job_type_skills": JSON,
            },
        )

        logger.info(
            "PostgreSQL load completed successfully for table '%s.%s'",
            POSTGRES_SCHEMA,
            POSTGRES_TABLE,
        )
    except Exception:
        logger.exception(
            "Failed to load dataframe into PostgreSQL table '%s.%s'",
            POSTGRES_SCHEMA,
            POSTGRES_TABLE,
        )
        raise
