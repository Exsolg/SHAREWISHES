from flask import (
    Blueprint,
    jsonify,
    make_response,
    redirect,
    render_template,
    request
)
from app.wishes.wish import Wish
from app.database import db


api = Blueprint('routes', __name__, template_folder='templates')


@api.errorhandler(404)
def err_handler():
    make_response(jsonify({'error': 'Page not found'}))


@api.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return redirect('/')

    query = request.form.get('search')
    all_wishes = db.session.query(Wish).all()
    all_wishes = list(filter(lambda wish: query.lower() in wish.title.lower() or query.lower() in wish.description.lower(), all_wishes))
    wish_list = [all_wishes[i:i + 3] for i in range(0, len(all_wishes), 3)]
    return render_template('index.html', title="Search", wish_list=wish_list)