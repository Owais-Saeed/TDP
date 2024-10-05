# __init__.py

import os
from flask import Flask, render_template
from .config import Config
# extensions
from .extensions import mongo, migrate, login_manager
# blueprints
from .blueprints.main import main_bp
from .blueprints.auth import auth_bp
from .blueprints.dashboard import dashboard_bp
# models
from .models.user import User
from bson.objectid import ObjectId

# the application factory
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialise extensions
    mongo.init_app(app)
    migrate.init_app(app, mongo)
    login_manager.init_app(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # blueprints
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    return app