from flask import (
    Blueprint,
    abort,
    redirect,
    render_template
)
from flask_login import current_user, login_required
from app.database import db
from app.users.user import User
from app.friends.friend import Friend
from app.wishes.wish import Wish
from sqlalchemy import and_, func, or_
from app.consts import *


friend_routes = Blueprint('friend_api', __name__, template_folder='templates')


@friend_routes.route('/add_friend/<string:username>', methods=['GET', 'POST'])
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


@friend_routes.route('/delete_friend/<string:username>', methods=['GET', 'POST'])
def delete_friend(username):
    user = db.session.query(User).filter(User.nick == username).first()
    friend = db.session.query(Friend).filter(or_(Friend.user_id == user.id, Friend.friend_id == user.id), or_(
        Friend.user_id == current_user.id, Friend.friend_id == current_user.id)).first()
    db.session.delete(friend)
    db.session.commit()
    return redirect(f'/@{user.nick}')


@friend_routes.route('/friends', methods=['GET', 'POST'])
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


@friend_routes.route('/notifications', methods=['GET', 'POST'])
def notifications():
    friends = []
    new_friends = db.session.query(Friend).filter(
        Friend.friend_id == current_user.id, Friend.relation_type == 'not_approved').all()
    for i in new_friends:
        user_friend = db.session.query(User).filter(
            User.id == i.user_id).first()
        friends.append(user_friend)
    return render_template('notifications.html', title="Notifications", friends=friends)


@friend_routes.route('/friends_ideas')
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
