import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal


from src.transform.data_transformer import (
    parse_job_skills_value,
    parse_job_type_skills_value,
    parse_semi_structured_columns,
)


def test_parse_job_skills_value_returns_list_of_strings():
    result = parse_job_skills_value("['sql', 'python']")

    assert result == ["sql", "python"]


def test_parse_job_skills_value_returns_empty_list_for_empty_string():
    result = parse_job_skills_value("")

    assert result == []


def test_parse_job_skills_value_returns_empty_list_for_nan():
    result = parse_job_skills_value(np.nan)

    assert result == []


def test_parse_job_skills_value_returns_empty_list_for_invalid_string():
    result = parse_job_skills_value("[sql, python]")

    assert result == []


def test_parse_job_type_skills_value_returns_dict():
    result = parse_job_type_skills_value("{'core': ['sql', 'python']}")

    assert result == {"core": ["sql", "python"]}


def test_parse_job_type_skills_value_returns_empty_dict_for_empty_string():
    result = parse_job_type_skills_value("")

    assert result == {}


def test_parse_job_type_skills_value_returns_empty_dict_for_nan():
    result = parse_job_type_skills_value(np.nan)

    assert result == {}


def test_parse_job_type_skills_value_returns_empty_dict_for_invalid_string():
    result = parse_job_type_skills_value("{core: ['sql']}")

    assert result == {}


def test_parse_semi_structured_columns_parses_expected_columns():
    input_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": ["['sql', 'python']", "['airflow']"],
            "job_type_skills": [
                "{'core': ['sql', 'python']}",
                "{'orchestration': ['airflow']}",
            ],
        }
    )

    expected_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": [["sql", "python"], ["airflow"]],
            "job_type_skills": [
                {"core": ["sql", "python"]},
                {"orchestration": ["airflow"]},
            ],
        }
    )

    result_df = parse_semi_structured_columns(input_df)

    assert_frame_equal(result_df, expected_df)


def test_parse_semi_structured_columns_handles_missing_values():
    input_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": ["['sql']", np.nan],
            "job_type_skills": ["{'core': ['sql']}", np.nan],
        }
    )

    expected_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": [["sql"], []],
            "job_type_skills": [{"core": ["sql"]}, {}],
        }
    )

    result_df = parse_semi_structured_columns(input_df)

    assert_frame_equal(result_df, expected_df)


def test_parse_semi_structured_columns_handles_invalid_values():
    input_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": ["[sql, python]", "['airflow']"],
            "job_type_skills": ["{core: ['sql']}", "{'orchestration': ['airflow']}"],
        }
    )

    expected_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "job_skills": [[], ["airflow"]],
            "job_type_skills": [{}, {"orchestration": ["airflow"]}],
        }
    )

    result_df = parse_semi_structured_columns(input_df)

    assert_frame_equal(result_df, expected_df)


def test_parse_semi_structured_columns_skips_missing_columns():
    input_df = pd.DataFrame(
        {
            "job_id": [1],
            "job_skills": ["['sql', 'python']"],
        }
    )

    expected_df = pd.DataFrame(
        {
            "job_id": [1],
            "job_skills": [["sql", "python"]],
        }
    )

    result_df = parse_semi_structured_columns(input_df)

    assert_frame_equal(result_df, expected_df)
