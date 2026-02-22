from app.core.deps import get_auth_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import (
    get_current_user
)
from app.models.user import User
from app.schemas.user import Login, Token, UserResponse, UserCreate

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    auth_service: Session = Depends(get_auth_service)
):
    """Registra um novo usuário"""

    created = auth_service.register(user_data)
    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    return created


@router.post("/login", response_model=Token)
async def login(
    form_data: Login,
    auth_service: Session = Depends(get_auth_service)
):
    """Autentica usuário e retorna token"""
    response = auth_service.login(form_data)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
