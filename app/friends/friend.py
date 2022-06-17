from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import db
from sqlalchemy_serializer import SerializerMixin


class Friend(db.Model, SerializerMixin):
    __tablename__ = 'friends'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    relation_type = Column(String(250), nullable=True, default='not_approved')

    def __repr__(self):
        return f'{self.friend_id}'