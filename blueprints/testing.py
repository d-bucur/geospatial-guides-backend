# Used for manually testing functionality. Should not be added to main app unless running in a test environment
import logging
from flask import Blueprint

from sql import db, models
tests = Blueprint('test_bp', __name__)


@tests.route('/test_user')
def test_user():
    return str(models.User.query.all())


@tests.route('/test_create')
def test_create():
    guest = models.User(username='guest', email='guest@example.com')
    db.session.add(guest)
    db.session.commit()
    return "created"


@tests.route('/error')
def throw_error():
    raise IndexError


@tests.route('/log_test')
def log_test():
    logging.debug("Test DEBUG")
    logging.info("Test INFO")
    logging.warning("Test WARN")
    logging.error("Test ERROR")
    return 'messages printed to std'
