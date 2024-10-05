from flask import render_template, redirect, url_for
from . import main_bp
from flask_login import current_user

@main_bp.route('/')
def index():
    # redirect user to dashboard if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('index.html')