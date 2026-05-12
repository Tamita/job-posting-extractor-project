import numpy as np

from src.transform.data_transformer import (
    parse_job_skills_value,
    parse_job_type_skills_value,
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
