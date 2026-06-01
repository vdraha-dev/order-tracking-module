from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.users.models import UserRole


class UserBase(BaseModel):
    username: str = Field(max_length=256)
    email: EmailStr
    role: UserRole = UserRole.User


class UserCreate(UserBase):
    password: str


class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    access_token: str
    expiry: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    expiry: datetime
