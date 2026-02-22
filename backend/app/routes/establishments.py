from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.core.deps import get_establishment_service
from app.schemas.establishment import (
    EstablishmentCreate,
    EstablishmentUpdate,
    EstablishmentResponse
)

router = APIRouter()


@router.post(
    "/",
    response_model=EstablishmentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_establishment(
    establishment_data: EstablishmentCreate,
    establishment_service: Session = Depends(get_establishment_service),
):
    """Cria um novo estabelecimento"""
    establishment = establishment_service.create(establishment_data)
    return establishment


@router.get("/", response_model=List[EstablishmentResponse])
async def list_establishments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    establishment_service: Session = Depends(get_establishment_service),
):
    """Lista todos os estabelecimentos com paginação"""
    establishments = establishment_service.get_all(skip=skip, limit=limit)
    return establishments


@router.get("/search", response_model=List[EstablishmentResponse])
async def search_establishments(
    name: str = Query(..., min_length=1),
    establishment_service: Session = Depends(get_establishment_service),
):
    """Busca estabelecimentos por nome"""
    establishments = establishment_service.search_by_name(name)
    return establishments


@router.get("/{establishment_id}", response_model=EstablishmentResponse)
async def get_establishment(
    establishment_id: int,
    establishment_service: Session = Depends(get_establishment_service),
):
    """Obtém um estabelecimento específico por ID"""
    establishment = establishment_service.get_by_id(establishment_id)
    if not establishment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    return establishment


@router.put("/{establishment_id}", response_model=EstablishmentResponse)
async def update_establishment(
    establishment_id: int,
    establishment_data: EstablishmentUpdate,
    establishment_service: Session = Depends(get_establishment_service),
):
    """Atualiza um estabelecimento"""
    establishment = establishment_service.update(
        establishment_id, establishment_data
    )
    if not establishment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    return establishment


@router.delete("/{establishment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_establishment(
    establishment_id: int,
    establishment_service: Session = Depends(get_establishment_service),
):
    """Deleta um estabelecimento"""
    success = establishment_service.delete(establishment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    return None
