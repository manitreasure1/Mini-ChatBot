from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    firstname: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class CreateUser(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Ensure password meets security requirements"""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v

    model_config = {"extra": "forbid"}


class CurrentUser(BaseModel):
    sub: str
    email: EmailStr
    exp: Optional[int] = None
    iat: Optional[int] = None
    refresh: Optional[bool] = False


class UpdateUser(BaseModel):
    firstname: Optional[str] = Field(None, min_length=2, max_length=50)
    lastname: Optional[str] = Field(None, min_length=2, max_length=50)
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class LoginUser(BaseModel):
    email: EmailStr
    password: str
    model_config = {"extra": "forbid"}


class SendMessage(BaseModel):
    message: str
    model_config = {"extra": "forbid"}


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str


class ChatMessageOut(BaseModel):
    message_id: UUID
    message: str
    response: str
    time_stamp: datetime

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    user_id: UUID
    firstname: str
    lastname: Optional[str] = None
    username: str
    email: EmailStr
    messages: List[ChatMessageOut] = []

    class Config:
        from_attributes = True