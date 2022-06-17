from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from sqlalchemy import func
from app.database import db
from app.wishes.wish import Wish

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('image', required=False, type=str)
parser.add_argument('link', required=False, type=str)
parser.add_argument('description', required=False, type=str)
parser.add_argument('is_private', required=False, type=int)


def edit_wish_arguments():
    parser.replace_argument('title', required=False)
    parser.replace_argument('user_id', required=False)


def add_wish_arguments():
    parser.replace_argument('title', required=True)
    parser.replace_argument('user_id', required=True)


def get_wish_or_abort(wishes_id):
    wish = db.session.query(Wish).get(wishes_id)
    if not wish:
        abort(404, message=f"Wish {wishes_id} not found")
    return wish


class WishesResource(Resource):
    def get(self, wish_id):
        wish = get_wish_or_abort(wish_id)
        return jsonify(wish.to_dict(only=('id', 'title', 'description', 'user_id', 'image', 'link', 'is_private')))

    def delete(self, wish_id):
        wish = get_wish_or_abort(wish_id)
        db.session.delete(wish)
        db.session.commit()
        return jsonify(wish.to_dict(only=('id', 'title', 'description', 'user_id', 'image', 'link', 'is_private')))

    def post(self):
        add_wish_arguments()
        args = parser.parse_args()
        wish = Wish(
            title=args['title'],
            user_id=args['user_id'],
            image=args['image'],
            link=args['link'],
            description=args['description'],
            is_private=args['is_private']
        )
        db.session.add(wish)
        db.session.commit()
        return jsonify(wish.to_dict(only=('id', 'title', 'description', 'user_id', 'image', 'link', 'is_private')))

    def put(self, wish_id):
        wish = get_wish_or_abort(wish_id)

        edit_wish_arguments()
        args = parser.parse_args()

        if 'title' in args:
            wish.title = args['title']
        if 'description' in args:
            wish.description = args['description']
        if 'image' in args:
            wish.image = args['image']
        if 'link' in args:
            wish.link = args['link']
        if 'is_private' in args:
            print(args['is_private'])
            wish.is_private = args['is_private']

        db.session.commit()
        return jsonify(wish.to_dict(only=('id', 'title', 'description', 'user_id', 'image', 'link', 'is_private')))


class WishesListResource(Resource):
    def get(self):
        edit_wish_arguments()
        filter = request.args
        wishes = db.session.query(Wish)
        if filter:
            if value := filter.get('user_id'):
                wishes = wishes.filter(Wish.user_id == value)
            if value := filter.get('title'):
                wishes = wishes.filter(func.lower(
                    Wish.title).like(f'%{value.lower()}%'))
            if value := filter.get('description'):
                wishes = wishes.filter(func.lower(
                    Wish.description).like(f'%{value.lower()}%'))
            if value := filter.get('is_private'):
                wishes = wishes.filter(Wish.is_private == value)

        return jsonify({'wishes': [item.to_dict(only=('id', 'title', 'description', 'user_id', 'image', 'link', 'is_private')) for item in wishes.all()]})
