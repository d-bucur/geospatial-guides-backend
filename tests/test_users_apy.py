from sql.models import User
from tests.datatype_assertions import assert_is_user


def test_get_user(client, base_db_session):
    user = User.query.first()
    r = client.get('/users/%d' % user.id)
    assert r.status_code == 200
    user_j = r.get_json()
    assert_is_user(user_j)


def test_invalid_user(client, base_db_session):
    r = client.get('/users/667')
    assert r.status_code == 404
    r = client.get('/users/sddshds')
    assert r.status_code == 404
