from src.load import normalization_loader as nl


def test_seed_skills_invokes_execute(monkeypatch):
    called = {}

    def fake_execute(sql_script, *, step_name):
        called["sql"] = sql_script
        called["step"] = step_name

    # Patch the execute_sql_script used by the loader helper
    monkeypatch.setattr(nl, "execute_sql_script", fake_execute)

    # Call the wrapper
    nl.seed_skills()

    assert called.get("step") == "seed_skills"
    assert "INSERT INTO skills" in called.get("sql", "")
