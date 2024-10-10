# blueprints/dashboard/routes.py
from itertools import filterfalse

from flask import render_template, redirect, url_for, flash, request, jsonify
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

    # transform decks into a dict to pass to the template
    decks_data = []
    for deck_item in decks:
        _deck = Deck(mongo.db, deck_item)
        print(_deck, flush=True)
        decks_data.append({
            'id': str(deck_item['_id']),
            'title': deck_item['title'],
            'card_count': _deck.get_card_count(),
        })

    return render_template(
        'dashboard/home.html',
        user=current_user,
        options_menu=options,
        data=decks_data,
        title=get_greeting(),
    )

@dashboard_bp.route('/deck/<id>', methods=['GET'])
@login_required
def deck(id):
    # fetch the deck
    deck = Deck.get_deck(mongo.db, id)

    # if deck doesn't exist
    if not deck:
        flash('Deck does not exist.', 'warning')
        return redirect(url_for('dashboard.home'))

    # if user does not have authentication to see the deck
    if ObjectId(deck['user_id']) != ObjectId(current_user.id):
        flash('You are not authorized to view this deck.', 'warning')
        return redirect(url_for('dashboard.home'))

    # transform decks into a dict to pass to the template
    deck_data = {
        'id': id,
        'level': deck.get('level'),
        'topic': deck.get('topic'),
        'units': []
    }
    for unit in deck.get('units', []):
        concepts = []
        for concept in unit['outline']:
            cards = []
            for card in concept['cards']:
                cards.append({'front': card['front'], 'back': card['back']})
            concepts.append({'concept': concept['concept'], 'cards': cards})
        deck_data['units'].append({
            'id': str(unit['id']),
            'title': unit['title'],
            'concepts': concepts,
        })

    return render_template(
        'dashboard/deck.html',
        user=current_user,
        options_menu=options,
        course=deck_data,
        title=deck.get('title'),
        back_url=url_for('dashboard.home'),
    )

@dashboard_bp.route('/deck/save_cards', methods=['POST'])
@login_required
def save_cards():
    new_data = request.get_json()
    print(new_data, flush=True)

    if not new_data:
        flash('No data received.', 'warning')
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    new_cards = request.get_json().get('cards')
    print(new_cards, flush=True)

    # get the deck
    deck_data = Deck.get_deck(mongo.db, new_data.get('id'))
    if not ObjectId(deck_data.get('user_id')) == ObjectId(current_user.id):
        flash('You do not have access to that deck.', 'warning')
        return jsonify({'status': 'error', 'message': 'You do not have access to that deck', 'redirect_url': url_for('dashboard.home')}), 400

    deck = Deck(mongo.db, deck_data)

    # create the new deck
    updated = False
    print(deck.units, flush=True)
    for unit in deck.units:
        if unit['title'] == new_data.get('unit'):
            for concept in unit['outline']:
                if concept['concept'] == new_data.get('concept'):
                    # update the concept's cards
                    concept['cards'].extend(new_cards)
                    updated = True
                    break
        if updated:
            break

    if not updated:
        print("not updated", flush=True)
        return jsonify({'status': 'error', 'message': 'Unit or concept not found'}), 404

    deck.save()

    flash(f'Cards added to "{deck.title}"!', 'success')
    return jsonify({'status': 'success', 'redirect_url': url_for('dashboard.deck', id=( ObjectId(deck.id) ))}), 200

@dashboard_bp.route('/new_deck', methods=['GET'])
@login_required
def new_deck():
    return render_template(
        'dashboard/new_deck.html',
        user=current_user,
        options_menu=options,
        title='New Deck',
        back_url=url_for('dashboard.home'),
    )

@dashboard_bp.route('/save_deck', methods=['POST'])
@login_required
def save_deck():
    new_deck_data = request.get_json()

    if not new_deck_data:
        flash('No data received.', 'warning')
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    # create the new deck
    new_deck = Deck(mongo.db)
    new_deck.user_id = current_user.id
    new_deck.title = new_deck_data['output']['topic']
    new_deck.topic = new_deck_data['output']['topic']
    new_deck.level = new_deck_data['output']['level']
    new_deck.units = new_deck_data['output']['units']
    for unit in new_deck.units:
        for concept in unit['outline']:
            concept['cards'] = []

    new_deck.save()

    flash(f'Deck "{new_deck.title}" has been created!', 'success')
    return jsonify({'status': 'success', 'redirect_url': url_for('dashboard.home')}), 200
