# blueprints/dashboard/routes.py

from flask import render_template
from . import dashboard_bp
from flask_login import login_required, current_user

options = [
    { 'name': 'Profile', 'url': '#', 'icon': 'bi-person-circle' },
    { 'name': 'Settings', 'url': '#', 'icon': 'bi-gear' },
    { 'name': 'Sign Out', 'url': '/auth/logout', 'icon': 'bi-box-arrow-right' },
]

@dashboard_bp.route('/', methods=['GET'])
@login_required
def home():
    return render_template(
        'dashboard/home.html',
        user=current_user,
        options_menu=options,
    )