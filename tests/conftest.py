import time

import pytest
from pytest_docker_tools import container

from config.login import USERNAME_KEY
from sql.models import User, Place, Guide


db_container = container(
    scope='session',
    image='kartoza/postgis:9.6-2.4',
    ports={
        '5432/tcp': '5432/tcp',
    },
    environment={
        'POSTGRES_USER': 'testuser',
        'POSTGRES_PASS': 'testpassword',
        'POSTGRES_DBNAME': 'testdb',
        'ALLOW_IP_RANGE': '0.0.0.0/0',
    }
)


@pytest.fixture(scope='session')
def app():
    from main import create_app
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'postgresql+pg8000://testuser:testpassword@/testdb',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': '=g-R_B?6q/7.(9c#',
        # 'SQLALCHEMY_ECHO': True, # Use when debugging
    })
    app.testing = True
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(scope='session')
def _db(app, db_container):
    from sql.models import db
    db.init_app(app)
    retries = 0
    while retries < 10:
        # If table creation fails retry it again after sleeping a few seconds.
        # The container might not be up and running yet
        try:
            db.create_all()
            return db
        except Exception:
            retries += 1
            time.sleep(2)
            print('Retrying connection to container db #%d' % retries)


@pytest.fixture(scope='function')
def db_session(_db, request):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    old_session = _db.session
    _db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()
        _db.session = old_session

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def base_db_session(db_session):
    example_user = User(name='admin', email='admin@example.com')
    db_session.add(example_user)
    db_session.commit()
    place_duomo = Place(name='Piazza Duomo')
    db_session.add(place_duomo)
    db_session.commit()

    db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=5.0,
        duration=15,
        download_link='',
        place_id=place_duomo.id,
        user_id=example_user.id
    ))
    db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=3.0,
        duration=5,
        download_link='',
        place_id=place_duomo.id,
        user_id=example_user.id
    ))
    db_session.commit()

    place_galleria = Place(name='Galleria Vittorio Emanuele')
    db_session.add(place_galleria)
    place_scala = Place(name='Teatro della Scala')
    db_session.add(place_scala)
    db_session.commit()
    return db_session


@pytest.fixture(scope='function')
def geospatial_db_session(db_session):
    example_user = User(name='admin', email='admin@example.com')
    db_session.add(example_user)
    db_session.commit()

    place_duomo = Place(
        name='Piazza Duomo',
        position='POINT(9.191948 45.464271)',
        tags='milano'
    )
    place_galleria = Place(
        name='Galleria Vittorio Emanuele',
        position='POINT(9.189915 45.465962)',
        tags='milano shopping'
    )
    place_scala = Place(
        name='Teatro della Scala',
        position='POINT(9.189508 45.467658)',
        tags='milano'
    )
    db_session.add(place_scala)
    db_session.add(place_galleria)
    db_session.add(place_duomo)
    db_session.commit()

    db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=5.0,
        duration=15,
        download_link='',
        place_id=place_duomo.id,
        user_id=example_user.id
    ))
    db_session.add(Guide(
        description='Breve descrizione della guida',
        price=1.0,
        rating=3.0,
        duration=5,
        download_link='',
        place_id=place_duomo.id,
        user_id=example_user.id
    ))
    db_session.commit()

    return db_session


@pytest.fixture(scope='function')
def login_fixture(client, base_db_session):
    client.post(
        '/users/login',
        json={
            USERNAME_KEY: 'admin@example.com'
        }
    )
