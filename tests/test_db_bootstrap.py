from src.load.db_bootstrap import ensure_database_exists


def test_ensure_database_exists_when_db_already_exists(monkeypatch):
    captured = {"queries": []}

    class FakeCursor:
        def execute(self, query, params=None):
            captured["queries"].append((query, params))

        def fetchone(self):
            return (1,)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def close(self):
            captured["closed"] = True

    def fake_connect(**kwargs):
        captured["connect_kwargs"] = kwargs
        return FakeConnection()

    monkeypatch.setattr("src.load.db_bootstrap.psycopg.connect", fake_connect)

    ensure_database_exists()

    assert captured["connect_kwargs"]["dbname"] == "postgres"
    assert captured["queries"][0][1] is not None
    assert captured["closed"] is True


def test_ensure_database_exists_creates_db_when_missing(monkeypatch):
    captured = {"queries": []}

    class FakeCursor:
        def __init__(self):
            self.fetch_count = 0

        def execute(self, query, params=None):
            captured["queries"].append((query, params))

        def fetchone(self):
            self.fetch_count += 1
            if self.fetch_count == 1:
                return None
            return None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def close(self):
            captured["closed"] = True

    def fake_connect(**kwargs):
        captured["connect_kwargs"] = kwargs
        return FakeConnection()

    monkeypatch.setattr("src.load.db_bootstrap.psycopg.connect", fake_connect)

    ensure_database_exists()

    assert captured["connect_kwargs"]["dbname"] == "postgres"
    assert len(captured["queries"]) == 2
    assert captured["closed"] is True
