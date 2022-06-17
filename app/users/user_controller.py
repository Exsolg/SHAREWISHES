import os
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request
)
from flask_login import AnonymousUserMixin, current_user, login_required, login_user, logout_user
from app.forms.data_changes import DataForm
from app.forms.private_info import PrivateForm
from app.forms.register_user import RegisterForm
from app.database import db
from app.forms.wish import WishForm
from app.users.user import Friend, User
from app.utils.utils import save_image
from app.wishes.wish import Wish
from sqlalchemy import and_, func, or_
from app.consts import *


user_routes = Blueprint('user_api', __name__, template_folder='templates')


@user_routes.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@user_routes.route("/login", methods=['POST'])
def login():
    form = request.form
    user = db.session.query(User).filter(
        or_(User.nick == form['username'], User.email == form['username'])).first()
    if user and user.check_password(form['password']):
        login_user(user, form.get('remember', False))
        return redirect("/")
    return abort(400)


@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Sign Up',
                                   form=form,
                                   message="Passwords don't match")
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Sign Up',
                                   form=form,
                                   message="User already exists")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.nick = form.nick.data
        user.email = form.email.data
        user.description = form.description.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, False)
        return redirect('/')
    return render_template('register.html', title='Sign Up', form=form)


@user_routes.route('/@<string:username>', methods=['GET', 'POST'])
def profile(username):
    user = db.session.query(User).filter(User.nick == username).first()
    friend = None

    if not user:
        return abort(404)

    if not isinstance(current_user, AnonymousUserMixin) and current_user.id == user.id:
        wishes = db.session.query(Wish).filter(Wish.user_id == user.id).all()
    else:
        wishes = db.session.query(Wish).filter(
            Wish.user_id == user.id, Wish.is_private == 0).all()

    if not isinstance(current_user, AnonymousUserMixin):
        friend = db.session.query(Friend).filter(or_(Friend.user_id == user.id, Friend.friend_id == user.id),
                                                 or_(Friend.user_id == current_user.id, Friend.friend_id == current_user.id)).first()

    wish_list = [wishes[i:i + 3] for i in range(0, len(wishes), 3)]

    edit_form = WishForm(prefix="edit")
    if edit_form.validate_on_submit():
        wish = db.session.query(Wish).get(edit_form.id.data)
        if edit_form.image.data:
            wish.image = save_image(edit_form.image.data, current_user.nick)
        for key, value in edit_form.data.items():
            if key == 'image' and not value.read():
                continue
            setattr(wish, key, value)
        db.session.commit()
        return redirect(f'/@{current_user.nick}')
    return render_template('profile.html', title="Profile", user_info=user, wish_list=wish_list, edit_form=edit_form, friend=friend)


@user_routes.route('/download_file', methods=["POST"])
def change_photo():
    path = os.path.join('sharewishes', 'app', 'static', 'img', 'users', current_user.nick)
    image = request.files["file"]
    ext = os.path.splitext(image.filename)[-1]

    if ext not in ['.jpg', '.gif', '.png']:
        abort(400)
    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, 'ava.png'), 'wb') as file:
        file.write(image.read())

    user_info = db.session.query(User).filter(
        User.id == current_user.id).first()
    if user_info:
        path = os.path.join('static', 'img', 'users', current_user.nick)
        user_info.image = os.path.join(path, 'ava.png')
        db.session.add(user_info)
        db.session.commit()
    return redirect('/')


@user_routes.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = DataForm()
    form1 = PrivateForm()
    if request.method == "GET":
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.age.data = user.age
            form.description.data = user.description
            form1.nick.data = user.nick
            form1.email.data = user.email

    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        if user:
            print(form.description.data)
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.description = form.description.data
            db.session.commit()
            return redirect(f'/@{user.nick}')
        else:
            abort(404)
    if form1.validate_on_submit():
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        if user:
            user.nick = form1.nick.data
            user.email = form1.email.data
            user.set_password(form1.password.data)
            db.session.commit()
            return redirect(f'/@{user.nick}')
        else:
            abort(404)
    return render_template('changes.html', title='Settings', form=form, form1=form1)


@user_routes.route('/add_friend/<string:username>', methods=['GET', 'POST'])
def add_friend(username):
    friend_info = db.session.query(User).filter(User.nick == username).first()
    friend_notes = db.session.query(Friend).filter(
        or_(Friend.user_id == friend_info.id,
            Friend.friend_id == friend_info.id),
        or_(Friend.user_id == current_user.id,
            Friend.friend_id == current_user.id)
    ).first()
    if friend_notes:
        friend_notes.relation_type = 'friend'
    else:
        friends = Friend()
        friends.user_id = current_user.id
        friends.friend_id = friend_info.id
        db.session.add(friends)

    db.session.commit()
    return redirect(f'/@{friend_info.nick}')


@user_routes.route('/delete_friend/<string:username>', methods=['GET', 'POST'])
def delete_friend(username):
    user = db.session.query(User).filter(User.nick == username).first()
    friend = db.session.query(Friend).filter(or_(Friend.user_id == user.id, Friend.friend_id == user.id), or_(
        Friend.user_id == current_user.id, Friend.friend_id == current_user.id)).first()
    db.session.delete(friend)
    db.session.commit()
    return redirect(f'/@{user.nick}')


@user_routes.route('/friends', methods=['GET', 'POST'])
def friends():
    user = db.session.query(User).filter(
        User.nick == current_user.nick).first()

    if not user:
        return abort(404)

    friends = []
    count_friends = None
    count_wishes = None

    friend = db.session.query(Friend).filter(or_(Friend.user_id == user.id, Friend.friend_id == user.id),
                                             or_(Friend.user_id == current_user.id,
                                                 Friend.friend_id == current_user.id), Friend.relation_type == 'friend').all()
    for i in friend:
        user_friend = db.session.query(User).filter(or_(
            User.id == i.friend_id, User.id == i.user_id), User.id != current_user.id).first()
        count_friends = db.session.query(func.count()).filter(
            or_(Friend.user_id == user_friend.id, Friend.friend_id == user_friend.id)).first()[0]
        count_wishes = db.session.query(func.count()).filter(
            Wish.user_id == user_friend.id).first()[0]
        friends.append(user_friend)

    return render_template('friends.html', title="Friends", friends=friends, count_friends=count_friends, count_wishes=count_wishes)


@user_routes.route('/notifications', methods=['GET', 'POST'])
def notifications():
    friends = []
    new_friends = db.session.query(Friend).filter(
        Friend.friend_id == current_user.id, Friend.relation_type == 'not_approved').all()
    for i in new_friends:
        user_friend = db.session.query(User).filter(
            User.id == i.user_id).first()
        friends.append(user_friend)
    return render_template('notifications.html', title="Notifications", friends=friends)


@user_routes.route('/friends_ideas')
@login_required
def friends_ideas():
    friends = []
    wishes = []
    friend_user = db.session.query(Friend).filter(
        current_user.id == Friend.user_id).all()
    for i in friend_user:
        friends.append(i.friend_id)
    friend_friend = db.session.query(Friend).filter(
        current_user.id == Friend.friend_id).all()
    for i in friend_friend:
        friends.append(i.user_id)
    for k in friends:
        wishes.append(db.session.query(Wish).filter(
            and_(Wish.is_private == 0, Wish.user_id == k)).first())
    wish_list = [list(filter(lambda x: x is not None, wishes[i:i + 3])) for i in range(0, len(wishes), 3)]
    return render_template('index.html', title="Friends wishes", wish_list=wish_list)


@user_routes.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return redirect('/')

    query = request.form.get('search')
    all_wishes = db.session.query(Wish).all()
    all_wishes = list(filter(lambda wish: query.lower() in wish.title.lower() or query.lower() in wish.description.lower(), all_wishes))
    wish_list = [all_wishes[i:i + 3] for i in range(0, len(all_wishes), 3)]
    return render_template('index.html', title="Search", wish_list=wish_list)
