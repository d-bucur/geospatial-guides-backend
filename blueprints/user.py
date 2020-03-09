import logging
import time

from flask import Blueprint, session, request, jsonify

from config.login import USERNAME_KEY, ID_TOKEN_KEY, CLIENT_ID
from sql import db
from sql.converters import to_object
from sql.models import User

from google.oauth2 import id_token
from google.auth.transport import requests

bp = Blueprint('user_bp', __name__)

# For more info on server side authentication check out the official docs
# https://developers.google.com/identity/protocols/OAuth2InstalledApp
# https://developers.google.com/identity/sign-in/android/backend-auth
# https://developers.google.com/identity/sign-in/web/server-side-flow

@bp.route("/tokensignin", methods=['POST'])
def tokensignin():
    data = request.get_json()
    token = data[ID_TOKEN_KEY]

    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    if not idinfo['email_verified']:
        raise ValueError('Email not verified')

    user_email = idinfo['email']
    expiration = idinfo['exp']
    current = time.time()
    # TODO add cookie expiry
    # if user is new create account. Then login
    user = User.query.filter(User.email == user_email).first()
    if user is None:
        user = User(name=user_email, email=user_email)
        db.session.add(user)
        db.session.commit()
        logging.info('Created user %d' % user.id)

    session[USERNAME_KEY] = user.id
    logging.info('Succesfully logged in user %d' % user.id)
    return 'ok'


@bp.route("/login", methods=['POST'])
def login():
    login_data = request.get_json()
    if login_data is None:
        logging.info('Received empty login data')
        return 'Login data is empty', 400

    usermail = login_data[USERNAME_KEY]
    user = User.query.filter(User.email == usermail).first()
    if user is None:
        logging.info('Referenced user not found in db')
        return '', 403

    session[USERNAME_KEY] = user.id
    logging.info('Succesfully logged in user %d' % user.id)
    return 'ok'


@bp.route("/logout", methods=['POST'])
def logout():
    if USERNAME_KEY in session:
        logging.info('Succesfully logged in user %d' % session[USERNAME_KEY])
        session.pop(USERNAME_KEY, None)
    else:
        logging.info('Logout for user that is not logged in')
        return 'User not logged in', 400
    return 'ok'


@bp.route("/<int:user_id>")
def guide(user_id):
    user_r = User.query.filter_by(id=user_id).first_or_404()
    return jsonify(to_object(user_r))
