from pathlib import Path

import pandas as pd
import pytest

from src.extract.data_extractor import read_raw_jobs_csv


def test_read_raw_jobs_csv_returns_dataframe(monkeypatch):
    expected_df = pd.DataFrame(
        {
            "job_id": [1, 2],
            "title": ["Data Engineer", "Analytics Engineer"],
        }
    )

    def mock_read_csv(file_path):
        return expected_df

    monkeypatch.setattr("src.extract.data_extractor.pd.read_csv", mock_read_csv)

    result = read_raw_jobs_csv(Path("fake/path/data_jobs.csv"))

    assert isinstance(result, pd.DataFrame)
    assert result.equals(expected_df)


def test_read_raw_jobs_csv_raises_exception_when_read_fails(monkeypatch):
    def mock_read_csv(file_path):
        raise FileNotFoundError("File not found")

    monkeypatch.setattr("src.extract.data_extractor.pd.read_csv", mock_read_csv)

    with pytest.raises(FileNotFoundError, match="File not found"):
        read_raw_jobs_csv(Path("fake/path/data_jobs.csv"))
