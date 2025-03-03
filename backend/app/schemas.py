from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class CreateUser(UserBase):
    password: str
    model_config = {'extra':'forbid'}
    

class UserPublic(UserBase):
    id: str


class UpdateUser(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password : Optional[str] = None

    

class LoginUser(BaseModel):
    email: EmailStr
    password: str
    model_config = {'extra':'forbid'}



class SendMessage(BaseModel):
    message:str
    model_config ={'extra': 'forbid'}




try:
    UpdateUser()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))