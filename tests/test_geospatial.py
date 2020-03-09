from sqlalchemy import func

from sql.models import Place

REF_POINT = 'POINT(9.189818 45.463292)'


def test_distance_query(geospatial_db_session):
    distances = geospatial_db_session\
        .query(Place,
               func.ST_Distance(REF_POINT, Place.position))\
        .all()
    assert len(distances) == 3
    duomo_dist = next(p for p in distances if p[0].name == 'Piazza Duomo')
    assert 190 < duomo_dist[1] < 200


def test_within_query(geospatial_db_session):
    nearby_places = geospatial_db_session\
        .query(Place)\
        .filter(func.ST_DWithin(
            Place.position,
            REF_POINT,
            300)
        ).all()
    assert len(nearby_places) == 2


def test_nearby_with_distances_query(geospatial_db_session):
    nearby_places = geospatial_db_session\
        .query(Place,
               func.ST_Distance(REF_POINT, Place.position).label('distance'))\
        .filter(func.ST_DWithin(
            Place.position,
            REF_POINT,
            300)
        ).order_by('distance')\
        .all()
    assert len(nearby_places) == 2
    assert nearby_places[1][0].name == 'Galleria Vittorio Emanuele'
    assert nearby_places[0][0].name == 'Piazza Duomo'


def test_nearby_with_count_query(geospatial_db_session):
    nearby_places = geospatial_db_session \
        .query(
            Place,
            func.ST_Distance(REF_POINT, Place.position).label('distance'),
            func.count(Place.guides)
        ).filter(func.ST_DWithin(
            Place.position,
            REF_POINT,
            300)
        ).outerjoin(Place.guides) \
        .group_by(Place.id) \
        .order_by('distance') \
        .all()
    assert len(nearby_places) == 2
    assert nearby_places[0][0].name == 'Piazza Duomo'
    assert nearby_places[0][2] == 2
    assert nearby_places[1][0].name == 'Galleria Vittorio Emanuele'
    assert nearby_places[1][2] == 0
