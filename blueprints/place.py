import logging

from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_

from sql import db
from sql.converters import to_object
from sql.models import Place

bp = Blueprint('place_bp', __name__)


@bp.route("/search")
def search():
    try:
        search_term = request.args.get('term').lower()
    except (TypeError, ValueError):
        logging.info('Missing search term')
        return 'Missing search term', 400

    try:
        lat = float(request.args.get('lat'))
        long = float(request.args.get('long'))
        current_pos = 'POINT(%f %f)' % (long, lat)
        return _search_with_position(current_pos, search_term)
    except (TypeError, ValueError):
        return _search_without_position(search_term)


def _search_with_position(current_pos, search_term):
    places_raw = db.session \
        .query(
            Place,
            func.ST_Distance(current_pos, Place.position).label('distance'),
            func.count(Place.guides)
        ).filter(or_(
            Place.name.ilike('%{}%'.format(search_term)),
            Place.tags.like('%{}%'.format(search_term))
        )) \
        .outerjoin(Place.guides) \
        .group_by(Place.id) \
        .order_by('distance') \
        .all()
    places = []
    for p_raw in places_raw:
        p = to_object(p_raw[0], excluded=['position'])
        p['numGuides'] = p_raw[2]
        p['distance'] = p_raw[1]
        places.append(p)

    logging.info('Returning %d results' % len(places))
    return jsonify(places)


def _search_without_position(search_term):
    places_raw = db.session \
        .query(
            Place,
            func.count(Place.guides)
        ).filter(or_(
            Place.name.ilike('%{}%'.format(search_term)),
            Place.tags.like('%{}%'.format(search_term))
        )) \
        .outerjoin(Place.guides) \
        .group_by(Place.id) \
        .all()
    places = []
    for p_raw in places_raw:
        p = to_object(p_raw[0], excluded=['position'])
        p['numGuides'] = p_raw[1]
        places.append(p)

    logging.info('Returning %d results' % len(places))
    return jsonify(places)


@bp.route("/nearby")
def nearby():
    try:
        lat = float(request.args.get('lat'))
        long = float(request.args.get('long'))
    except (TypeError, ValueError):
        logging.info('Missing latitude and longitude params')
        return 'Missing latitude and longitude params', 400

    dist = int(request.args.get('distance') or 350)
    current_pos = 'POINT(%f %f)' % (long, lat)

    places_raw = db.session \
        .query(
            Place,
            func.ST_Distance(current_pos, Place.position).label('distance'),
            func.count(Place.guides)
        ).filter(func.ST_DWithin(
            Place.position,
            current_pos,
            dist)
        ).outerjoin(Place.guides) \
        .group_by(Place.id) \
        .order_by('distance') \
        .all()

    places = []
    for p_raw in places_raw:
        p = to_object(p_raw[0], excluded=['position'])
        p['numGuides'] = p_raw[2]
        p['distance'] = p_raw[1]
        places.append(p)

    logging.info('Returning %d results' % len(places))
    return jsonify(places)


@bp.route("/<int:place_id>/guides")
def guides(place_id):
    place = Place.query.filter_by(id=place_id).first_or_404()
    guides_for_place = place.guides
    logging.info('Returning %d results' % len(guides_for_place))
    return jsonify(to_object(guides_for_place, excluded=['full_text', 'download_link']))
