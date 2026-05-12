import logging

from .utils.logging_config import setup_logging
from .extract.pipeline import run_pipeline

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Application started")

    try:
        df = run_pipeline()
        logger.info(
            "Application finished successfully with %s records",
            len(df),
        )
    except Exception:
        logger.exception("Application execution failed")
        raise


if __name__ == "__main__":
    main()
