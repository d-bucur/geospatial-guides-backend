import pytest

from sql.models import User, Place, Guide


def test_add_two_users(base_db_session):
    assert len(User.query.all()) == 1
    user = User(name='user', email='user@example.com')
    guest = User(name='guest', email='guest@example.com')
    base_db_session.add(user)
    base_db_session.add(guest)
    base_db_session.commit()
    users = User.query.all()
    assert len(users) == 3
    ret_user = User.query.filter_by(name='user').first()
    assert ret_user.id == user.id


def test_add_one_user(base_db_session):
    assert len(User.query.all()) == 1
    guest = User(name='guest', email='guest@example.com')
    base_db_session.add(guest)
    base_db_session.commit()
    ret_user = User.query.filter_by(name='guest').first()
    assert ret_user.id == guest.id
    

def test_add_places(base_db_session):
    place_duomo = Place(name='Piazza Duomo')
    base_db_session.add(place_duomo)
    base_db_session.add(Place(name='Galleria Vittorio Emanuele'))
    base_db_session.add(Place(name='Teatro della Scala'))
    base_db_session.commit()


def test_add_guides(base_db_session):
    place_scala = Place.query.filter(Place.name == 'Teatro della Scala').first()
    assert len(place_scala.guides) == 0
    test_user = User.query.first()

    base_db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=5.0,
        duration=15,
        download_link='',
        place_id=place_scala.id,
        user_id=test_user.id
    ))
    base_db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=3.0,
        duration=5,
        download_link='',
        place_id=place_scala.id,
        user_id=test_user.id
    ))
    base_db_session.commit()

    assert len(place_scala.guides) == 2


# TODO test queries
