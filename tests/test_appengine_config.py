from importlib import reload
import config.sql


def test_appengine_sql_connection(monkeypatch):
    monkeypatch.setattr(config, 'running_on_appengine', lambda: True)
    reload(config.sql)
    assert '?unix_sock=/cloudsql/' in config.sql.URI


def test_local_sql_connection():
    import config.sql
    reload(config.sql)
    assert '?unix_sock=/cloudsql/' not in config.sql.URI

