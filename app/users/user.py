from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from app.database import db
from flask_login import UserMixin
from app.login_manager import login_manager
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nick = Column(String, nullable=False, unique=True)
    age = Column(DateTime, nullable=True)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<User {self.nick}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
