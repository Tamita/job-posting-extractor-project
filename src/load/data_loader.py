import logging

import pandas as pd
from sqlalchemy import JSON

from src.config.settings import POSTGRES_SCHEMA, POSTGRES_TABLE
from src.load.db_connector import create_postgres_engine

logger = logging.getLogger(__name__)


def load_jobs_to_postgres(df: pd.DataFrame) -> None:
    logger.info(
        "Starting PostgreSQL load for table '%s.%s'",
        POSTGRES_SCHEMA,
        POSTGRES_TABLE,
    )

    try:
        engine = create_postgres_engine()

        df.to_sql(
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
