from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import and_, or_
from app.database import db
from app.friends.friend import Friend
from app.users.user import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('nick', required=True)
parser.add_argument('age', required=False)
parser.add_argument('email', required=True)


def get_friends_or_abort(user_id):
    friends = db.session.query(Friend).filter(
        or_(Friend.user_id == user_id, Friend.friend_id == user_id)).all()
    if not friends:
        abort(404, message=f"User {user_id} hasn't friends")
    return friends


def get_friend_note_or_abort(user_id, friend_id):
    note = db.session.query(Friend).filter(and_(or_(Friend.user_id == user_id, Friend.friend_id == user_id), or_(
        Friend.user_id == friend_id, Friend.friend_id == friend_id))).first()
    if not note:
        abort(404, message=f"User {user_id} isn't friend with User {friend_id}")
    return note

class FriendsResource(Resource):
    def get(self, user_id):
        if user_id:
            friends = get_friends_or_abort(user_id)
        else:
            friends = db.session.query(Friend).all()
        return jsonify({'friends': [friend.to_dict(
                only=('surname', 'name', 'nick', 'age', 'email')) for friend in friends]})

    def delete(self, user_id, friend_id):
        user = get_friend_note_or_abort(user_id, friend_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': 'OK'})

    def post(self, user_id, friend_id):
        friend = Friend(
            user_id=user_id,
            friend_id=friend_id
        )
        db.session.add(friend)
        db.session.commit()
        return jsonify({'success': 'OK'})
