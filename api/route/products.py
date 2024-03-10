from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import Swagger
from api.schema.welcome import WelcomeSchema
from api.model.model import Product, Comment
from database import db
import json
from pprint import pprint
from werkzeug.datastructures import MultiDict
from api.helper.social_provider import create_mastodon_post, mastodon_status, create_mastodon_comment
from api.helper.open_ai import generate_hashtags, generate_campaign_post, generate_comment_post
import time   
 
BRAND_NAME = "ifo"
CAMPAIGN_GOAL = "Help us Kickstart AI Startups with the Power of Community and Crypto"

product_api = Blueprint('product_api', __name__, url_prefix='/api')
comment_api = Blueprint('comment_api', __name__, url_prefix='/api')

@product_api.route('/products', methods=['GET'])
def get_products():
    # resp = mastodon_status("112065853322040361")
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@product_api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.serialize())

@product_api.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.json
        # Validate that the required fields are present in the request
        required_fields = ['company_name', 'company_email', 'product_title', 'product_url', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        product_url = data["product_url"]
        existing_product = Product.query.filter_by(product_url=product_url).first()
        # pprint(existing_product.unique_tag)
        # pprint(existing_product.post_id)
        if existing_product is not None:
            return jsonify({'error': f'This product is already exist: {product_url}'}), 400


        product = Product(**data)
        generated_hashtag = generate_hashtags(project_title=product.product_title, project_description=product.description)
        epoch_time = int(time.time())
        unique_tag = f"{generated_hashtag}{BRAND_NAME.capitalize()}{epoch_time}"
        
        new_hashtags = f"#{BRAND_NAME} {generated_hashtag} {unique_tag}"

        generated_content = generate_campaign_post(product.product_title,product.description,product.product_url,CAMPAIGN_GOAL, new_hashtags)
        resp = create_mastodon_post(generated_content)

        # print(resp)
        product.common_tags = new_hashtags
        product.unique_tag = unique_tag
        product.post_id = resp.id
        product.platform = "mastodon"
        product.gen_description = generated_content
        
        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product created successfully', 'id': product.id, 'post_id':product.post_id }), 201

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error creating product: {str(e)}")

        return jsonify({'error': 'Internal Server Error'}), 500



@comment_api.route('/comment', methods=['POST'])
def process_comment():
    try:
        data = request.json

        if not data:
            return jsonify({'error': 'Empty request body or invalid JSON'}), 400

        parent_post_id = data.get("parent_id")

        if parent_post_id is not None:
            product = Product.query.filter_by(post_id=parent_post_id).first()

            if product is not None:
                comment = Comment(**data)
                comment_post, sentiment = generate_comment_post(product.gen_description, comment.comment_id)
                comment_post = f"@{comment.username} {comment_post}"

                resp = create_mastodon_comment(comment_post, comment.comment_id)

                if resp is None:
                    return jsonify({'error': 'Mastodon post failed'}), 400

                comment.reply_message = comment_post
                comment.reply_message_id = resp.id
                comment.sentiment = sentiment
                print("comment reply")
                print(comment)
                db.session.add(comment)
                status = db.session.commit()
                print(status)
                return jsonify({'message': 'Comment created successfully', 'id': comment.id, "comment_id": comment.comment_id}), 201
            else:
                return jsonify({'error': 'Product not found'}), 400

        return jsonify({'error': 'This is not the comment'}), 400

    except Exception as e:
        # Log the error for debugging purposes
        print(e)
        print(f"Error creating product: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
@comment_api.route('/comments', methods=['GET'])
def get_comments():
    # resp = mastodon_status("112065853322040361")
    comments = Comment.query.all()
    print(comments)
    return jsonify([comment.serialize() for comment in comments])

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