from flask import jsonify
from flask_restful import Resource, abort, reqparse
from app.database import db
from app.users.user import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('nick', required=True)
parser.add_argument('age', required=False)
parser.add_argument('email', required=True)


def get_user_or_abort(user_id):
    user = db.session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user


class UsersResource(Resource):
    def get(self, user_id):
        user = get_user_or_abort(user_id)
        return jsonify(user.to_dict(
            only=('surname', 'name', 'nick', 'age', 'email')))

    def delete(self, user_id):
        user = get_user_or_abort(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        user = db.session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('surname', 'name', 'nick', 'age', 'email')) for item in user]})

    def post(self):
        args = parser.parse_args()
        user = User(
            surname=args['surname'],
            name=args['name'],
            nick=args['nick'],
            age=args['age'],
            email=args['email']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': 'OK'})
