import logging

from flask import Blueprint, jsonify, session

from config.login import USERNAME_KEY
from sql import db
from sql.converters import to_object
from sql.models import Guide, User

bp = Blueprint('guide_bp', __name__)


@bp.route("/<int:guide_id>")
def guide(guide_id):
    guide_r = Guide.query.filter_by(id=guide_id).first_or_404()
    return jsonify(to_object(guide_r, excluded=['full_text', 'download_link']))


@bp.route("/<int:guide_id>/download")
def download(guide_id):
    if USERNAME_KEY not in session:
        logging.info('User not logged in')
        return 'User not logged in', 403
    user = User.query.filter(User.id == session[USERNAME_KEY]).first()
    Guide.query.filter(Guide.id == guide_id).first_or_404()
    for guide_r in user.purchased_guides:
        if guide_r.id == guide_id:
            logging.info('User %d correctly downloaded guide' % user.id)
            return jsonify(to_object(guide_r, selected=['full_text', 'download_link']))

    logging.info('User %d has not purchased guide' % user.id)
    return 'Guide not purchased. Unauthorized', 403


@bp.route("/<int:guide_id>/purchase", methods=['POST'])
def purchase(guide_id):
    if USERNAME_KEY not in session:
        logging.info('User not logged in. Cannot purchase')
        return 'User not logged in. Cannot purchase', 403
    user_r = User.query.filter(User.id == session[USERNAME_KEY]).first()
    for g in user_r.purchased_guides:
        if g.id == guide_id:
            logging.info('Guide already purchased')
            return 'Guide already purchased', 400
    guide_r = Guide.query.filter_by(id=guide_id).first_or_404()
    user_r.purchased_guides.append(guide_r)
    db.session.add(user_r)
    db.session.commit()
    logging.info('User %d correctly purchased guide' % user_r.id)
    return 'Correctly purchased', 200
