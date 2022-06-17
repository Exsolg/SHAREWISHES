from flask import (
    Blueprint,
    abort,
    jsonify,
    make_response,
    redirect,
    request,
    render_template
)
from flask_login import current_user, login_required
from app.database import db
from app.utils.utils import save_image
from app.wishes.wish import Wish

wish_routes = Blueprint('wishes_api', __name__, template_folder='templates')


@wish_routes.route('/')
def index():
    wishes = db.session.query(Wish).filter(Wish.is_private == 0).all()
    wish_list = [wishes[i:i + 3] for i in range(0, len(wishes), 3)]
    return render_template('index.html', title="Wishes", wish_list=wish_list)


@wish_routes.route("/add_wish", methods=['POST'])
@login_required
def add_wish():
    form = request.form
    wish = Wish()
    wish.user_id = current_user.id
    if not form['title'] or not form['description']:
        abort(400)
        
    if request.files.get('add-image'):
        wish.image = save_image(request.files['add-image'], current_user.nick)
        
    for key, value in form.items():
        if key == 'add-image':
            continue
        setattr(wish, key, value)
    db.session.add(wish)
    db.session.commit()
    return make_response(jsonify({'success': 'ok'}), 200)