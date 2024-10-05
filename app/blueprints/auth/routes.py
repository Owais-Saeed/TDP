# blueprints/auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from app.extensions import mongo
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from .forms import RegistrationForm
from bson.objectid import ObjectId

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle login
        # email = request.form['email']
        email = request.form.get('email')
        # password = request.form['password']
        password = request.form.get('password')
        user_data = mongo.db.users.find_one({'email': email})
        if user_data and User.verify_password(user_data, password):
            user = User(user_data)
            login_user(user)
            flash('You are logged in.', 'success')
            return redirect(url_for('dashboard.dashboard_home'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        # check if the email already exists
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('auth.register'))

        # hash the password
        hashed_password = User.hash_password(password)

        # insert the user into mongo
        user_id = mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        }).inserted_id

        # create a user object
        user = User({
            '_id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password
        })

        # log the user in
        login_user(user)
        flash('You are registered.', 'success')
        return redirect(url_for('dashboard.dashboard_home'))

    return render_template('auth/register.html', form=form)