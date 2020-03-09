from sql.models import Guide
from tests.datatype_assertions import assert_is_downloaded_guide


def test_download_guide_without_login(client):
    r = client.get('/guides/1/download')
    assert r.status_code == 403


def test_purchase_guide_without_login(client):
    r = client.post('/guides/1/purchase')
    assert r.status_code == 403


def test_guide_download_authenticated_not_purchased(client, login_fixture):
    guide = Guide.query.first()
    r = client.get('/guides/%d/download' % guide.id)
    assert r.status_code == 403


def test_guide_purchase_and_download(client, login_fixture):
    guide = Guide.query.first()

    r = client.get('/guides/%d/download' % guide.id)
    assert r.status_code == 403

    r = client.post('/guides/%d/purchase' % guide.id)
    assert r.status_code == 200

    r = client.get('/guides/%d/download' % guide.id)
    assert r.status_code == 200
    guide = r.get_json()
    assert_is_downloaded_guide(guide)


def test_guide_double_purchase(client, login_fixture):
    guide = Guide.query.first()

    r = client.post('/guides/%d/purchase' % guide.id)
    assert r.status_code == 200

    r = client.post('/guides/%d/purchase' % guide.id)
    assert r.status_code == 400
