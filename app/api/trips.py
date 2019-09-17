from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from flask import g, abort, jsonify, request, url_for
from app.models import Trip


@bp.route('/trips/<int:id>', methods=['GET'])
@token_auth.login_required
def get_trip(id):
    return jsonify(Trip.query.get_or_404(id).to_dict())


@bp.route('/trips', methods=['GET'])
@token_auth.login_required
def get_trips():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Trip.to_collection_dict(Trip.query.order_by(Trip.timestamp.desc()), page, per_page, 'api.get_trips')
    return jsonify(data)


@bp.route('/trips', methods=['POST'])
@token_auth.login_required
def create_trip():
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title field')
    data['user_id'] = g.current_user.id
    trip = Trip()
    trip.from_dict(data)
    db.session.add(trip)
    db.session.commit()
    response = jsonify(trip.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_trip', id=trip.id)
    return response

@bp.route('/trips/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_trip(id):
    trip = Trip.query.get_or_404(id)
    if g.current_user.id != trip.user_id:
        abort(403)
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title field')
    trip.from_dict(data)
    db.session.commit()
    return jsonify(trip.to_dict())