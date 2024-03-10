from flask import Flask
from api.route.campaign import campaign_api
from api.route.fan import fan_api
from api.route.products import product_api, comment_api
from database import db
from flask_migrate import Migrate
import pandas as pd
from dash_app import create_dash_app
from flask_cors import CORS

# Define the Flask app creation function
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Config
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifo.db'
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(campaign_api)
    app.register_blueprint(fan_api)
    app.register_blueprint(product_api)
    app.register_blueprint(comment_api)

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    flask_app = create_app()
    dash_app = create_dash_app(flask_app)
    # dash_app = hello_world_dash(flask_app)

    flask_app.run(host="0.0.0.0", port=port, debug=True)