from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from app.database import db
from sqlalchemy_serializer import SerializerMixin
import datetime


class Wish(db.Model, SerializerMixin):
    __tablename__ = 'wishes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image = Column(String, nullable=True)
    link = Column(String, nullable=True)
    description = Column(String(250), nullable=True)
    is_private = Column(Boolean, nullable=False, default=False)
    created_date = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", backref="wishes")

    def __repr__(self):
        return f"<Wish {self.title}>"
