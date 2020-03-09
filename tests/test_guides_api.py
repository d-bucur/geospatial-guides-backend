import pytest

from sql.models import Place, Guide
from tests.datatype_assertions import assert_is_guide, assert_is_downloaded_guide


def test_healthcheck(client):
    r = client.get('/status')
    assert r.status_code == 200


def test_get_single_guide(client, base_db_session):
    guide = Guide.query.first()
    r = client.get('/guides/%d' % guide.id)
    assert r.status_code == 200
    guide = r.get_json()
    assert_is_guide(guide)


def test_get_inexistent_guide(client):
    r = client.get('/guides/500')
    assert r.status_code == 404


def test_download_inexistent_guide(client, login_fixture):
    r = client.get('/guides/500/download')
    assert r.status_code == 404


def test_get_invalid_guide_id(client):
    r = client.get('/guides/invalid')
    assert r.status_code == 404
    r = client.get('/guides/invalid/download')
    assert r.status_code == 404


