from pathlib import Path
import pandas as pd
import logging
from src.config.settings import RAW_JOBS_FILE

logger = logging.getLogger(__name__)

def read_raw_jobs_csv(file_path: Path = RAW_JOBS_FILE) -> pd.DataFrame:
    logger.info("Starting CSV read from %s", file_path)
    df = pd.read_csv(file_path)
    logger.info("CSV loaded successfully with %s rows and %s columns", len(df), len(df.columns))
    return df
