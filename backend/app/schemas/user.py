from app.enums import RoleEnum
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str
    full_name: str | None = None
    role: RoleEnum = RoleEnum.inspector


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Login(BaseModel):
    email: str
    password: str
