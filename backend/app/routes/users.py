from typing import List
from sqlalchemy.orm import Session
from app.core.deps import get_user_service
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    user_service: Session = Depends(get_user_service)
):
    """Lista todos os usuários (requer autenticação)"""
    users = user_service.get_users(skip, limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    user_service: Session = Depends(get_user_service)
):
    """Obtém um usuário específico por ID"""
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user
