from flask import Flask
from api.resources.metar import metar_resource


# Create and configure the app
def create_app():
    # Create an instance of Flask
    app = Flask(__name__)

    # Load the instance config from settings module
    app.config.from_pyfile('settings.py')

    # Register /api/v1/metar routes
    app.register_blueprint(metar_resource, url_prefix='/api/v1/metar/')

    return app
