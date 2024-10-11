import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI')
    LANGSERVE_API_URL = os.environ.get('LANGSERVE_API_URL')
    # debug
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True