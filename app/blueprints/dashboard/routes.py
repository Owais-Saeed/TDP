# blueprints/dashboard/routes.py

from flask import render_template, redirect, url_for, flash, request
from . import dashboard_bp
from flask_login import login_required, current_user
from app.extensions import mongo
from app.models.deck import Deck
from .forms import CreateDeckForm
from bson.objectid import ObjectId
# get the time
from datetime import datetime
import pytz
# for API requests
import requests

options = [
    { 'name': 'Profile', 'url': '#', 'icon': 'bi-person-circle' },
    { 'name': 'Settings', 'url': '#', 'icon': 'bi-gear' },
    { 'name': 'Sign Out', 'url': '/auth/logout', 'icon': 'bi-box-arrow-right' },
]

def get_greeting():
    # pleasant greeting
    timezone = pytz.timezone('Australia/Melbourne')
    now = datetime.now(timezone)
    current_hour = now.hour

    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

@dashboard_bp.route('/', methods=['GET'])
@login_required
def home():
    # fetch sets for current user from mongodb
    decks = Deck.get_decks_by_user(mongo.db, current_user.id)

    # transform sets into a dict to pass to the template
    decks_data = []
    for deck_item in decks:
        decks_data.append({
            'id': str(deck_item['_id']),
            'title': deck_item['title'],
            'card_count': deck_item.get('card_count', 0),
        })

    return render_template(
        'dashboard/home.html',
        user=current_user,
        options_menu=options,
        data=decks_data,
        title=get_greeting(),
    )

@dashboard_bp.route('/new_deck', methods=['GET', 'POST'])
@login_required
def new_deck():
    form = CreateDeckForm()

    if form.validate_on_submit():
        title = request.form.get('title')

        if not title:
            flash('Title is required.', 'warning')
            return redirect(url_for('dashboard.new_deck'))

        # create the new deck
        new_deck = Deck(mongo.db)
        new_deck.title = title
        new_deck.units = []
        new_deck.user_id = current_user.id
        new_deck.card_count = 0
        new_deck.save()

        flash(f'Deck "{title}" has been created!', 'success')
        return redirect(url_for('dashboard.home'))

    return render_template(
        'dashboard/new_deck.html',
        user=current_user,
        options_menu=options,
        form=form,
        title='New Deck',
        back_url=url_for('dashboard.home'),
    )