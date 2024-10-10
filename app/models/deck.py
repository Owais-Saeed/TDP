# models/deck.py
import pymongo
from bson.objectid import ObjectId
from .user import User
from datetime import datetime, timezone

class Deck:
    def __init__(self, mongo_db, data=None):
        self.mongo_db = mongo_db
        if data:
            self.id = str(data.get('_id'))
            self.title = data.get('title')
            self.topic = data.get('topic')
            self.level = data.get('level')
            self.units = data.get('units', [])
            self.user_id = data.get('user_id')
            self.created_at = data.get('created_at', datetime.now(timezone.utc))
        else:
            self.id = None
            self.title = ''
            self.topic = ''
            self.level = ''
            self.units = []
            self.user_id = ''
            self.created_at = datetime.now(timezone.utc)

    def save(self):
        deck_data = {
            'title': self.title,
            'topic': self.topic,
            'level': self.level,
            'units': self.units,
            'user_id': ObjectId(self.user_id),
            'created_at': self.created_at,
        }
        if self.id:
            # update existing set
            self.mongo_db.decks.update_one({'_id': ObjectId(self.id)}, {'$deck': deck_data})
        else:
            # create new set
            result = self.mongo_db.decks.insert_one(deck_data)
            self.id = str(result.inserted_id)

    @staticmethod
    def get_decks_by_user(mongo_db, user_id):
        decks = mongo_db.decks.find({'user_id': ObjectId(user_id)}).sort('created_at', -1)
        return decks

    @staticmethod
    def get_deck(mongo_db, deck_id):
        return mongo_db.decks.find_one({'_id': ObjectId(deck_id)})

    def get_card_count(self):
        total_cards = 0
        for unit in self.units:
            for concept in unit.get('outline', []):
                total_cards += len(concept.get('cards', []))
        return total_cards