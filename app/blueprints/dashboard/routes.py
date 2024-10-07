# blueprints/dashboard/routes.py

from flask import render_template, redirect, url_for, flash, request
from . import dashboard_bp
from flask_login import login_required, current_user
from app.extensions import mongo
from app.models.deck import Deck
from .forms import CreateDeckForm
from bson.objectid import ObjectId

options = [
    { 'name': 'Profile', 'url': '#', 'icon': 'bi-person-circle' },
    { 'name': 'Settings', 'url': '#', 'icon': 'bi-gear' },
    { 'name': 'Sign Out', 'url': '/auth/logout', 'icon': 'bi-box-arrow-right' },
]

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
    )

@dashboard_bp.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    if request.method == 'POST':
        title = request.form.get('title')

        if not title:
            flash('Title is required.', 'warning')
            return redirect(url_for('dashboard.create_deck'))

        # create the new deck
        new_deck = Deck(mongo.db)
        new_deck.title = title
        new_deck.user_id = current_user.id
        new_deck.card_count = 0
        new_deck.save()

        flash(f'Deck "{title}" has been created!', 'success')
        return redirect(url_for('dashboard.home'))

    form = CreateDeckForm()
    return render_template('dashboard/create_deck.html', user=current_user, form=form)