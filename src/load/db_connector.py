import logging
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine

from src.config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

logger = logging.getLogger(__name__)


def build_postgres_connection_url() -> str:
    """Build a SQLAlchemy URL for ``postgresql+psycopg`` using settings.

    Returns:
        Connection string with the password URL-encoded for special characters.
    """
    encoded_password = quote_plus(POSTGRES_PASSWORD)

    return (
        f"postgresql+psycopg://{POSTGRES_USER}:{encoded_password}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def create_postgres_engine() -> Engine:
    """Create a new SQLAlchemy ``Engine`` for the configured PostgreSQL database.

    Returns:
        Engine bound to ``build_postgres_connection_url()``.

    Raises:
        Exception: Engine creation failures are logged and re-raised.
    """
    connection_url = build_postgres_connection_url()

    logger.info("Creating PostgreSQL engine for database '%s'", POSTGRES_DB)

    try:
        engine = create_engine(connection_url)
        logger.info("PostgreSQL engine created successfully")
        return engine
    except Exception:
        logger.exception("Failed to create PostgreSQL engine")
        raise
