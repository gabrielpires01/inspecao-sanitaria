from datetime import timedelta
from app.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_data: UserCreate):
        db_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()

        if db_user:
            return None

        hashed_password = get_password_hash(user_data.password)
        print(hashed_password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def login(self, form_data: OAuth2PasswordRequestForm):
        user: User | None = self.db.query(User).filter(User.email == form_data.email).first()

        if not user or not verify_password(form_data.password, user.hashed_password):
            return None

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
