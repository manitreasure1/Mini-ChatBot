from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, ForeignKey, DateTime, func
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List
from pydantic import ValidationError


class Users(db.Model):
    user_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    firstname : Mapped[str] = mapped_column(String(length=15))
    lastname : Mapped[str] = mapped_column(String(length=15))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash : Mapped[str] = mapped_column(String)
    messages:Mapped[List['ChatMessage']] = relationship('ChatMessage', back_populates='user')

    @staticmethod
    def get_user_by_id(user_id):
        user_obj = db.session.get(Users, user_id)
        return user_obj
    
    @validates('username')
    def validate_username(self, key, username: str)-> str:
        if db.session.query(Users).filter_by(username = username).first():
            raise ValueError('User Already Exist!')
        return username
    
    @validates('email')
    def validate_email(self, key, email: str)-> str:
        if db.session.query(Users).filter_by(email = email).first():
            raise ValueError('Email Already Exist!')
        return email


class ChatMessage(db.Model):
    message_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    message: Mapped[str] = mapped_column(String)
    response : Mapped[str] = mapped_column(String)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.user_id'), nullable=True)
    time_stamp: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    user:Mapped['Users'] = relationship('Users', back_populates='messages')



