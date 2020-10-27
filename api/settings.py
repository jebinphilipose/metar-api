from os import environ

FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')
FLASK_RUN_PORT = environ.get('FLASK_RUN_PORT')
SECRET_KEY = environ.get('SECRET_KEY')
REDIS_HOST = environ.get('REDIS_HOST')
REDIS_PORT = environ.get('REDIS_PORT')
