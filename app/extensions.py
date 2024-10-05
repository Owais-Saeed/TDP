# extensions.py

from flask_pymongo import PyMongo
from flask_migrate import Migrate
from flask_login import LoginManager

mongo = PyMongo()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'