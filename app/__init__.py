from flask import Flask
from flask_migrate import Migrate
from app.database import db
from flask_restful import Api
from app.login_manager import login_manager
from app.wishes.wishes_resource import WishesListResource, WishesResource
from app.users.users_resources import UsersListResource, UsersResource
from app.routes import api as route
from app.users.user_controller import user_routes
from app.wishes.wishes_controller import wish_routes
import os
from app.consts import *


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(route)
    app.register_blueprint(user_routes)
    app.register_blueprint(wish_routes)
    api = Api(app)
    login_manager.init_app(app)

    api.add_resource(WishesListResource, API_V1_URI + '/wishes')
    api.add_resource(WishesResource, API_V1_URI + '/wish/<int:wish_id>', API_V1_URI + '/wish')
    api.add_resource(UsersListResource, API_V1_URI + '/users')
    api.add_resource(UsersResource, API_V1_URI + '/user/<int:user_id>', API_V1_URI + '/user')

    db.init_app(app)
    migrate = Migrate(app, db)
    with app.test_request_context():
        db.create_all()

    return app
