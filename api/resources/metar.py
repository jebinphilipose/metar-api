from flask import Blueprint

metar_resource = Blueprint('metar', __name__)


@metar_resource.route('/ping')
def ping():
    return {'data': 'pong'}, 200
