import jmespath

from sql.models import Place
from tests.datatype_assertions import assert_is_place, assert_is_guide, assert_is_place_without_distance


def test_place_search_full(client, geospatial_db_session):
    r = client.get('/places/search?term=Milano&lat=%f&long=%f' % (45.463292, 9.189818))
    assert r.status_code == 200
    places_for_milano = r.get_json()
    assert len(places_for_milano) > 0
    for p in places_for_milano:
        assert_is_place(p)
    place_names = jmespath.search('[].name', places_for_milano)
    assert 'Piazza Duomo' in place_names
    assert 'Galleria Vittorio Emanuele' in place_names
    assert 'Teatro della Scala' in place_names


def test_place_search_no_position(client, geospatial_db_session):
    r = client.get('/places/search?term=Milano')
    assert r.status_code == 200
    places_for_milano = r.get_json()
    assert len(places_for_milano) > 0
    for p in places_for_milano:
        assert_is_place_without_distance(p)
    place_names = jmespath.search('[].name', places_for_milano)
    assert 'Piazza Duomo' in place_names
    assert 'Galleria Vittorio Emanuele' in place_names
    assert 'Teatro della Scala' in place_names


def test_place_search_by_tag(client, geospatial_db_session):
    r = client.get('/places/search?term=shopping')
    assert r.status_code == 200
    places_for_milano = r.get_json()
    assert len(places_for_milano) > 0
    for p in places_for_milano:
        assert_is_place_without_distance(p)
    place_names = jmespath.search('[].name', places_for_milano)
    assert 'Galleria Vittorio Emanuele' in place_names


def test_place_no_result(client, geospatial_db_session):
    r = client.get('/places/search?term=Sarmisegetusa')
    assert r.status_code == 200
    places = r.get_json()
    assert len(places) == 0


def test_invalid_place_id(client):
    r = client.get('/places/invalid/guides')
    assert r.status_code == 404


def test_inexistent_place_id(client):
    r = client.get('/places/300/guides')
    assert r.status_code == 404


def test_place_with_guides(client, base_db_session):
    place_duomo = Place.query.filter(Place.name.ilike('%duomo%')).first()
    r = client.get('/places/%d/guides' % place_duomo.id)
    assert r.status_code == 200
    guides_for_duomo = r.get_json()
    assert len(guides_for_duomo) > 0
    for g in guides_for_duomo:
        assert_is_guide(g)


def test_empty_guides_for_place(client, base_db_session):
    place_scala = Place.query.filter(Place.name.ilike('%scala%')).first()
    r = client.get('/places/%d/guides' % place_scala.id)
    assert r.status_code == 200
    guides = r.get_json()
    assert len(guides) == 0


def test_nearby_places_invalid_params(client, geospatial_db_session):
    r = client.get('/places/nearby?lat=9.189818')
    assert r.status_code == 400
    r = client.get('/places/nearby?long=45.463292')
    assert r.status_code == 400
    r = client.get('/places/nearby?lat=adc&long=fdc&distance=300')
    assert r.status_code == 400


def test_nearby_places(client, geospatial_db_session):
    r = client.get('/places/nearby?lat=%f&long=%f&distance=300' % (45.463292, 9.189818))
    assert r.status_code == 200
    places = r.get_json()
    assert len(places) == 2
    for p in places:
        assert_is_place(p)
        assert p['distance'] < 300

    r = client.get('/places/nearby?lat=%f&long=%f' % (45.463292, 9.189818))
    assert r.status_code == 200
    places = r.get_json()
    assert len(places) > 0
    for p in places:
        assert_is_place(p)

    r = client.get('/places/nearby?lat=%f&long=%f&distance=1' % (45.463292, 9.189818))
    assert r.status_code == 200
    places = r.get_json()
    assert len(places) == 0
