import pandas as pd
import pytest

from src.extract.pipeline import run_pipeline


def test_run_pipeline_returns_dataframe(monkeypatch):
    expected_df = pd.DataFrame(
        {
            "job_id": [1, 2, 3],
            "title": ["DE", "DA", "DS"],
        }
    )

    def mock_read_raw_jobs_csv():
        return expected_df

    monkeypatch.setattr(
        "src.extract.pipeline.read_raw_jobs_csv",
        mock_read_raw_jobs_csv,
    )

    result = run_pipeline()

    assert isinstance(result, pd.DataFrame)
    assert result.equals(expected_df)


def test_run_pipeline_raises_exception_when_extractor_fails(monkeypatch):
    def mock_read_raw_jobs_csv():
        raise ValueError("Invalid CSV format")

    monkeypatch.setattr(
        "src.extract.pipeline.read_raw_jobs_csv",
        mock_read_raw_jobs_csv,
    )

    with pytest.raises(ValueError, match="Invalid CSV format"):
        run_pipeline()
