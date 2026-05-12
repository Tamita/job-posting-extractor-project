import logging

from .utils.logging_config import setup_logging
from .extract.data_extractor import read_raw_jobs_csv
from .transform.data_transformer import parse_semi_structured_columns

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Application started")

    try:
        df = read_raw_jobs_csv()
        
        parsed_df = parse_semi_structured_columns(df)

        if parsed_df.empty:
            logger.warning("Application completed with an empty dataset")
        else:
            logger.info(
                "Application execution finished successfully with %s records",
                len(parsed_df),
            )
    except Exception:
        logger.exception("Application execution failed")
        raise


if __name__ == "__main__":
    main()
