import pandas as pd

from src.load.data_loader import load_jobs_to_postgres


def test_load_jobs_to_postgres_calls_to_sql(monkeypatch):
    captured = {}

    class FakeEngine:
        pass

    def fake_create_postgres_engine():
        return FakeEngine()

    def fake_to_sql(self, name, con, schema, if_exists, index, **kwargs):
        captured["name"] = name
        captured["con"] = con
        captured["schema"] = schema
        captured["if_exists"] = if_exists
        captured["index"] = index
        captured["dtype"] = kwargs.get("dtype")

    monkeypatch.setattr(
        "src.load.data_loader.create_postgres_engine",
        fake_create_postgres_engine,
    )
    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql)

    df = pd.DataFrame(
        {
            "job_title": ["Data Engineer"],
            "company_name": ["ACME"],
        }
    )

    load_jobs_to_postgres(df)

    assert captured["name"] == "raw_jobs"
    assert captured["schema"] == "public"
    assert captured["if_exists"] == "replace"
    assert captured["index"] is False
    assert isinstance(captured["con"], FakeEngine)
    assert "job_skills" in captured["dtype"]
    assert "job_type_skills" in captured["dtype"]
