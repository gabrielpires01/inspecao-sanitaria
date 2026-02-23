from app.enums import RoleEnum
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from starlette.middleware.base import BaseHTTPMiddleware

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def convert_str_to_byte(string):
    return string.encode("utf-8")


def hash_string(bytes):
    return bcrypt.hashpw(bytes, bcrypt.gensalt(12))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = convert_str_to_byte(plain_password)
    hashed_bytes = convert_str_to_byte(hashed_password.strip())

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(
        convert_str_to_byte(password), bcrypt.gensalt(12)
    )
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str | None = payload.get("sub")
        role: int | None = payload.get("role")
        if email is None:
            raise credentials_exception
        return email, role
    except JWTError:
        raise credentials_exception


def get_credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = get_credentials_exception()

    email, _role = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception
    return user


PUBLIC_ROUTES = [
    "/api/auth/login",
    "/api/auth/register",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/",
    "/health",
]

SUPERUSER_ROUTES = [
    ("/api/establishments", "DELETE"),
    ("/api/inspections", "DELETE"),
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Não foi possível validar as credenciais"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            token = auth.split(" ")[1]
            credentials_exception = get_credentials_exception()
            email, role = verify_token(token, credentials_exception)
            if not email:
                return JSONResponse(
                    {"detail": "Não foi possível validar as credenciais"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

            url_method = (request.url.path, request.method)
            if url_method in SUPERUSER_ROUTES and role != RoleEnum.superuser.value:
                return JSONResponse(
                    {"detail": "Usuário não possui autorização suficiente"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

        except (HTTPException, JWTError, IndexError, ValueError):
            return JSONResponse(
                {"detail": "Não foi possível validar as credenciais"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return await call_next(request)
