# models/user.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.name = user_data.get('name')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password')

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
