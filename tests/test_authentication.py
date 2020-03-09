from flask import session

from config.login import USERNAME_KEY


def test_login_and_logout(client, base_db_session):
    with client:
        client.get('/')
        assert USERNAME_KEY not in session

        r = client.post(
            '/users/login',
            json={
                USERNAME_KEY: 'admin@example.com'
            }
        )
        assert r.status_code == 200
        assert USERNAME_KEY in session

        r = client.post('/users/logout')
        assert r.status_code == 200
        assert USERNAME_KEY not in session


def test_login_fail(client, base_db_session):
    with client:
        r = client.post(
            '/users/login',
            json={
                USERNAME_KEY: 'inexistent@example.com'
            }
        )
        assert r.status_code == 403
        assert USERNAME_KEY not in session


def test_double_logout(client, login_fixture):
    with client:
        r = client.post('/users/logout')
        assert r.status_code == 200
        assert USERNAME_KEY not in session

        r = client.post('/users/logout')
        assert r.status_code == 400
        assert USERNAME_KEY not in session
