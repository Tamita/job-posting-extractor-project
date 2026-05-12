import logging

import psycopg
from psycopg import sql

from src.config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = logging.getLogger(__name__)


def ensure_database_exists() -> None:
    logger.info("Checking if PostgreSQL database '%s' exists", POSTGRES_DB)

    conn = psycopg.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        autocommit=True,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (POSTGRES_DB,),
            )
            exists = cur.fetchone()

            if exists:
                logger.info("Database '%s' already exists", POSTGRES_DB)
                return

            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(POSTGRES_DB))
            )
            logger.info("Database '%s' created successfully", POSTGRES_DB)
    finally:
        conn.close()
