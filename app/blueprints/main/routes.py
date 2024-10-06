from flask import render_template, redirect, url_for, flash
from . import main_bp
from flask_login import current_user

@main_bp.route('/')
def home():
    '''
    flash('Welcome.', 'success')
    flash('Welcome.', 'danger')
    flash('Welcome.', 'warning')
    flash('Welcome.', 'info')
    '''
    # redirect user to dashboard if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('home.html')