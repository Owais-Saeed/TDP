# blueprints/dashboard/__init__.py

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

from . import routes
