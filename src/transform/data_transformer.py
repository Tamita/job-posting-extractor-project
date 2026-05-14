import ast
from typing import Any
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def parse_job_skills_value(value: Any) -> list[str]:
    """Parse a single CSV cell into a list of skill strings.

    Uses ``ast.literal_eval`` when the value looks like a Python list literal.
    Returns an empty list for null/empty values, non-lists, or parse failures.

    Args:
        value: Raw cell value (often a string representation of a list).

    Returns:
        List of skill names as strings.
    """
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
    """Parse a single CSV cell into a dict of job-type skill groupings.

    Uses ``ast.literal_eval`` when the value looks like a Python dict literal.
    Returns an empty dict for null/empty values, non-dicts, or parse failures.

    Args:
        value: Raw cell value (often a string representation of a dict).

    Returns:
        Parsed mapping, or an empty dict when parsing is not possible.
    """
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
    """Return a copy of ``df`` with ``job_skills`` / ``job_type_skills`` parsed in place.

    Columns are only transformed when present. Other columns are unchanged.

    Args:
        df: Raw dataframe straight from CSV.

    Returns:
        Dataframe with list/dict Python objects in the semi-structured columns.
    """
    parsed_df = df.copy()

    if "job_skills" in parsed_df.columns:
        parsed_df["job_skills"] = parsed_df["job_skills"].apply(parse_job_skills_value)

    if "job_type_skills" in parsed_df.columns:
        parsed_df["job_type_skills"] = parsed_df["job_type_skills"].apply(
            parse_job_type_skills_value
        )

    return parsed_df
