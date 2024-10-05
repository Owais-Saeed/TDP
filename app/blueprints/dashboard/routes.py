# blueprints/dashboard/routes.py

from flask import render_template
from . import dashboard_bp
from flask_login import login_required, current_user

@dashboard_bp.route('/', methods=['GET'])
@login_required
def home():
    return render_template('dashboard/home.html', user=current_user)