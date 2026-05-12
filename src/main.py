import logging

from .utils.logging_config import setup_logging
from .extract.data_extractor import read_raw_jobs_csv
from .transform.data_transformer import parse_semi_structured_columns
from .transform.raw_jobs_schema import validate_raw_jobs_dataframe
from .load.data_loader import load_jobs_to_postgres
from .load.db_bootstrap import ensure_database_exists

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Starting jobs ETL pipeline")

    ensure_database_exists()

    raw_df = read_raw_jobs_csv()
    parsed_df = parse_semi_structured_columns(raw_df)
    validated_df = validate_raw_jobs_dataframe(parsed_df)
    load_jobs_to_postgres(validated_df)

    logger.info("Jobs ETL pipeline completed successfully")


if __name__ == "__main__":
    main()
