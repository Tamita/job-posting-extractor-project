"""Pandera schema and helpers for validating parsed raw job dataframes."""

import pandas as pd
import pandera.pandas as pa
from pandera import Check


def is_list_value(value: object) -> bool:
    """Return True if ``value`` is a Python ``list`` (used by Pandera column checks)."""
    return isinstance(value, list)


def is_dict_value(value: object) -> bool:
    """Return True if ``value`` is a Python ``dict`` (used by Pandera column checks)."""
    return isinstance(value, dict)


raw_jobs_schema = pa.DataFrameSchema(
    {
        "job_title_short": pa.Column(str, nullable=True, required=True),
        "job_title": pa.Column(str, nullable=True, required=True),
        "job_location": pa.Column(str, nullable=True, required=True),
        "company_name": pa.Column(str, nullable=True, required=True),
        "job_work_from_home": pa.Column(bool, nullable=True, required=True),
        "job_no_degree_mention": pa.Column(bool, nullable=True, required=True),
        "job_health_insurance": pa.Column(bool, nullable=True, required=True),
        "job_skills": pa.Column(
            object,
            checks=Check(lambda s: s.map(is_list_value)),
            nullable=True,
            required=True,
        ),
        "job_type_skills": pa.Column(
            object,
            checks=Check(lambda s: s.map(is_dict_value)),
            nullable=True,
            required=True,
        ),
    },
    strict=False,
    coerce=False,
)


def validate_raw_jobs_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate ``df`` against ``raw_jobs_schema``.

    Args:
        df: Parsed jobs dataframe (see ``parse_semi_structured_columns``).

    Returns:
        The validated dataframe (same data when validation succeeds).

    Raises:
        pandera.errors.SchemaErrors: When required columns or checks fail.
    """
    return raw_jobs_schema.validate(df)
