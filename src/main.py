import logging
from .utils.logging_config import setup_logging
from .extract.pipeline import run_pipeline

logger = logging.getLogger(__name__)

def main() -> None:
    setup_logging()
    logger.info("Pipeline execution started")
    df =  run_pipeline()
    logger.info("Pipeline execution finished successfully with %s records", len(df))

if __name__ == "__main__":
    main()