from fastapi import Depends
from app.core.database import get_db
from app.services.users import UserService
from app.services.auth import AuthService


def get_user_service(db=Depends(get_db)) -> UserService:
    return UserService(db=db)


def get_auth_service(db=Depends(get_db)) -> AuthService:
    return AuthService(db=db)
