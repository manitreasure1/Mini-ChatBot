from datetime import datetime
from pydantic import EmailStr
import uuid
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Users(SQLModel, table=True):
    user_id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str
    username: str = Field(unique=True, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    password_hash: str
    messages: List["ChatMessage"] = Relationship(
        back_populates="user", cascade_delete=True
    )


class ChatMessage(SQLModel, table=True):
    message_id: uuid.UUID = Field(default=None, primary_key=True)
    message: str
    response: str
    user_id: uuid.UUID = Field(
        nullable=True, foreign_key="users.user_id", ondelete="CASCADE"
    )
    time_stamp: datetime = Field(default_factory=datetime.now)
    user: Users = Relationship(back_populates="messages")



