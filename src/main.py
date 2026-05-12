import logging

from .utils.logging_config import setup_logging
from .extract.data_extractor import read_raw_jobs_csv
from .transform.data_transformer import parse_semi_structured_columns
from .transform.raw_jobs_schema import validate_raw_jobs_dataframe
from .load.data_loader import load_jobs_to_postgres

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Application started")

    try:
        df = read_raw_jobs_csv()
        parsed_df = parse_semi_structured_columns(df)
        validated_df = validate_raw_jobs_dataframe(parsed_df)

        if validated_df.empty:
            logger.warning("Application completed with an empty dataset")
            return

        load_jobs_to_postgres(validated_df)

        logger.info(
            "Application execution finished successfully with %s records",
            len(validated_df),
        )
    except Exception:
        logger.exception("Application execution failed")
        raise


if __name__ == "__main__":
    main()
