from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import Swagger
from api.schema.welcome import WelcomeSchema
from api.model.model import Campaign
from database import db


campaign_api = Blueprint('campaign_api', __name__, url_prefix='/api')

@campaign_api.route('/campaigns', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.all()
    return jsonify([campaign.serialize() for campaign in campaigns])

@campaign_api.route('/campaigns/<int:id>', methods=['GET'])
def get_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    return jsonify(campaign.serialize())

@campaign_api.route('/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    campaign = Campaign(**data)
    db.session.add(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign created successfully', 'id': campaign.id}), 201

@campaign_api.route('/campaigns/<int:id>', methods=['PUT'])
def update_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(campaign, key, value)
    db.session.commit()
    return jsonify({'message': 'Campaign updated successfully'})

@campaign_api.route('/campaigns/<int:id>', methods=['DELETE'])
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted successfully'})