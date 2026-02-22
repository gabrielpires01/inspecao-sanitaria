from typing import List
from app.schemas.user import UserResponse
from app.models.user import User
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[UserResponse]:
        users = self.db.query(User).offset(skip).limit(limit).all()
        return users

    def get_user(
        self,
        user_id
    ) -> UserResponse:
        user = self.db.get(User, user_id)
        return user
