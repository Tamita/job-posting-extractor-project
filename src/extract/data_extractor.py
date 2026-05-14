from pathlib import Path
import logging

import pandas as pd

from src.config.settings import RAW_JOBS_FILE

logger = logging.getLogger(__name__)


def read_raw_jobs_csv(file_path: Path = RAW_JOBS_FILE) -> pd.DataFrame:
    """Load the raw jobs dataset from CSV into a pandas DataFrame.

    Args:
        file_path: Path to the CSV file. Defaults to ``RAW_JOBS_FILE`` from settings.

    Returns:
        DataFrame with one row per job posting.

    Raises:
        Exception: Any error from ``pandas.read_csv`` is logged and re-raised.
    """
    logger.info("Starting CSV read from %s", file_path)

    try:
        df = pd.read_csv(file_path)
        logger.info(
            "CSV loaded successfully with %s rows and %s columns",
            len(df),
            len(df.columns),
        )
        return df
    except Exception:
        logger.exception("Failed to read raw jobs CSV from %s", file_path)
        raise
