from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import Swagger
from api.schema.welcome import WelcomeSchema
from api.model.model import Product
from database import db
import json
from pprint import pprint
from werkzeug.datastructures import MultiDict
from api.helper.social_provider import create_mastodon_post, mastodon_status

product_api = Blueprint('product_api', __name__, url_prefix='/api')

@product_api.route('/products', methods=['GET'])
def get_products():
    resp = mastodon_status("112065853322040361")
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@product_api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.serialize())


@product_api.route('/products', methods=['POST'])
def create_product():
    try:
        print()
        data = request.json
        # Validate that the required fields are present in the request
        required_fields = ['company_name', 'company_email', 'product_title', 'product_url', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            
        product = Product(**data)
        
        hashtags = "#ifo"
        resp = create_mastodon_post(product.description, hashtags, product.product_url )

        print(resp)
        
        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product created successfully', 'id': product.id}), 201

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error creating product: {str(e)}")

        return jsonify({'error': 'Internal Server Error'}), 500


## If we need form data with file then the api will change using below one
# @product_api.route('/products/form', methods=['POST'])
# def create_product_form():
#     try:
#         form_data = MultiDict(request.form)

#         # Validate that the required fields are present in the form data
#         required_fields = ['company_name', 'company_email', 'product_title', 'product_logo', 'product_url', 'description', 'twitter_username']
#         for field in required_fields:
#             if field not in form_data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400

#         # Create a Product instance using form data
#         product = Product(**form_data)
        
#         # Add the product to the database
#         db.session.add(product)
#         db.session.commit()

#         return jsonify({'message': 'Product created successfully', 'id': product.id}), 201

#     except Exception as e:
#         # Log the error for debugging purposes
#         print(f"Error creating product: {str(e)}")

#         return jsonify({'error': 'Internal Server Error'}), 500
    
@product_api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@product_api.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})