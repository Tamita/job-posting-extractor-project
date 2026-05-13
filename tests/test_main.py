import pandas as pd

from src.main import main


def test_main_runs_full_pipeline(monkeypatch):
    calls = []

    raw_df = pd.DataFrame({"job_title": ["Data Engineer"]})
    parsed_df = pd.DataFrame({"job_title": ["Data Engineer"], "job_skills": [[]]})
    validated_df = pd.DataFrame({"job_title": ["Data Engineer"], "job_skills": [[]]})

    def fake_setup_logging():
        calls.append("setup_logging")

    def fake_ensure_database_exists():
        calls.append("ensure_database_exists")

    def fake_read_raw_jobs_csv():
        calls.append("read_raw_jobs_csv")
        return raw_df

    def fake_parse_semi_structured_columns(df):
        calls.append("parse_semi_structured_columns")
        assert df is raw_df
        return parsed_df

    def fake_validate_raw_jobs_dataframe(df):
        calls.append("validate_raw_jobs_dataframe")
        assert df is parsed_df
        return validated_df

    def fake_load_jobs_to_postgres(df):
        calls.append("load_jobs_to_postgres")
        assert df is validated_df

    def fake_create_normalized_schema():
        calls.append("create_normalized_schema")

    def fake_seed_reference_entities():
        calls.append("seed_reference_entities")

    def fake_seed_locations():
        calls.append("seed_locations")

    def fake_seed_skills():
        calls.append("seed_skills")

    def fake_seed_jobs():
        calls.append("seed_jobs")

    def fake_seed_job_skills():
        calls.append("seed_job_skills")

    monkeypatch.setattr("src.main.setup_logging", fake_setup_logging)
    monkeypatch.setattr("src.main.ensure_database_exists", fake_ensure_database_exists)
    monkeypatch.setattr("src.main.read_raw_jobs_csv", fake_read_raw_jobs_csv)
    monkeypatch.setattr(
        "src.main.parse_semi_structured_columns",
        fake_parse_semi_structured_columns,
    )
    monkeypatch.setattr(
        "src.main.validate_raw_jobs_dataframe",
        fake_validate_raw_jobs_dataframe,
    )
    monkeypatch.setattr("src.main.load_jobs_to_postgres", fake_load_jobs_to_postgres)
    monkeypatch.setattr(
        "src.main.create_normalized_schema",
        fake_create_normalized_schema,
    )
    monkeypatch.setattr(
        "src.main.seed_reference_entities",
        fake_seed_reference_entities,
    )
    monkeypatch.setattr("src.main.seed_locations", fake_seed_locations)
    monkeypatch.setattr("src.main.seed_skills", fake_seed_skills)
    monkeypatch.setattr("src.main.seed_jobs", fake_seed_jobs)
    monkeypatch.setattr("src.main.seed_job_skills", fake_seed_job_skills)

    main()

    assert calls == [
        "setup_logging",
        "ensure_database_exists",
        "read_raw_jobs_csv",
        "parse_semi_structured_columns",
        "validate_raw_jobs_dataframe",
        "load_jobs_to_postgres",
        "create_normalized_schema",
        "seed_reference_entities",
        "seed_locations",
        "seed_skills",
        "seed_jobs",
        "seed_job_skills",
    ]
