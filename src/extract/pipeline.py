import logging

from .data_extractor import read_raw_jobs_csv

logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Pipeline execution started")

    try:
        df = read_raw_jobs_csv()

        if df.empty:
            logger.warning("Pipeline completed with an empty dataset")
        else:
            logger.info(
                "Pipeline execution finished successfully with %s records",
                len(df),
            )

        return df
    except Exception:
        logger.exception("Pipeline execution failed")
        raise
