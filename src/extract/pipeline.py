import logging
from .data_extractor import read_raw_jobs_csv

logger = logging.getLogger(__name__)

def run_pipeline() -> None:
    logger.info("Pipeline execution started")
    df = read_raw_jobs_csv()
    logger.info("Pipeline execution finished successfully with %s records", len(df))
    return df
