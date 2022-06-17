from flask import (
    Blueprint,
    jsonify,
    make_response
)
api = Blueprint('routes', __name__, template_folder='templates')


@api.errorhandler(404)
def err_handler():
    make_response(jsonify({'error': 'Page not found'}))