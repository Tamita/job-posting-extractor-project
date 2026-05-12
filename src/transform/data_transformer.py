import ast
from typing import Any
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def parse_job_skills_value(value: Any) -> list[str]:
    if value is None or value == "" or pd.isna(value):
        return []

    try:
        parsed_value = ast.literal_eval(value)

        if not isinstance(parsed_value, list):
            logger.warning("job_skills value is not a list: %s", value)
            return []

        return [str(item) for item in parsed_value]

    except (ValueError, SyntaxError, TypeError):
        logger.warning("Failed to parse job_skills value: %s", value)
        return []


def parse_job_type_skills_value(value: Any) -> dict:
    if value is None or value == "" or pd.isna(value):
        return {}

    try:
        parsed_value = ast.literal_eval(value)

        if not isinstance(parsed_value, dict):
            logger.warning("job_type_skills value is not a dict: %s", value)
            return {}

        return parsed_value

    except (ValueError, SyntaxError, TypeError):
        logger.warning("Failed to parse job_type_skills value: %s", value)
        return {}


def parse_semi_structured_columns(df: pd.DataFrame) -> pd.DataFrame:
    parsed_df = df.copy()

    if "job_skills" in parsed_df.columns:
        parsed_df["job_skills"] = parsed_df["job_skills"].apply(parse_job_skills_value)

    if "job_type_skills" in parsed_df.columns:
        parsed_df["job_type_skills"] = parsed_df["job_type_skills"].apply(
            parse_job_type_skills_value
        )

    return parsed_df
