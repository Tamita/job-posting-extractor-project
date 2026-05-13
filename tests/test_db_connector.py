from src.load.db_connector import (
    build_postgres_connection_url,
    create_postgres_engine,
)


def test_build_postgres_connection_url_returns_postgres_url():
    result = build_postgres_connection_url()

    assert result.startswith("postgresql+psycopg://")
    assert "@" in result
    assert "/" in result


def test_create_postgres_engine_calls_create_engine(monkeypatch):
    captured = {}

    class FakeEngine:
        pass

    def fake_create_engine(connection_url):
        captured["connection_url"] = connection_url
        return FakeEngine()

    monkeypatch.setattr("src.load.db_connector.create_engine", fake_create_engine)

    result = create_postgres_engine()

    assert isinstance(result, FakeEngine)
    assert captured["connection_url"].startswith("postgresql+psycopg://")
