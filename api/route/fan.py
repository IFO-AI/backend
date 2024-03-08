from http import HTTPStatus
from flask import Blueprint, jsonify, request
from api.model.model import Fan

fan_api = Blueprint('fan_api', __name__, url_prefix='/api')
from database import db

@fan_api.route('/fans', methods=['GET'])
def get_campaigns():
    fans = Fan.query.all()
    return jsonify([fan.serialize() for fan in fans])


@fan_api.route('/fans', methods=['POST'])
def add_fan():
    data = request.json
    email = data.get('email')
    interests = data.get('interests')
    engagement_level = data.get('engagement_level')

    if not email or not interests or not engagement_level:
        return jsonify({'message': 'Missing required fields'}), 400

    if Fan.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_fan = Fan(email=email, interests=interests, engagement_level=engagement_level)
    db.session.add(new_fan)
    db.session.commit()

    return jsonify({'message': 'Fan added successfully'}), 201

