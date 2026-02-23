from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.core.deps import get_inspection_service
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.inspection import (
    InspectionCreate,
    InspectionCreateService,
    InspectionUpdate,
    InspectionResponse
)

router = APIRouter()


@router.post(
    "/",
    response_model=InspectionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_inspection(
    inspection_data: InspectionCreate,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova inspeção"""
    dict_data = dict(inspection_data)

    inspection = inspection_service.create(InspectionCreateService(
        **dict_data,
        inspector_id=current_user.id
    ))
    return inspection


@router.get("/", response_model=List[InspectionResponse])
async def list_inspections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as inspeções com paginação"""
    inspections = inspection_service.get_all(skip=skip, limit=limit)
    return inspections


@router.get(
    "/establishment/{establishment_id}",
    response_model=List[InspectionResponse]
)
async def get_inspections_by_establishment(
    establishment_id: int,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Busca inspeções por estabelecimento"""
    inspections = inspection_service.get_by_establishment(establishment_id)
    return inspections


@router.get(
    "/inspector/{inspector_id}",
    response_model=List[InspectionResponse]
)
async def get_inspections_by_inspector(
    inspector_id: int,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Busca inspeções por inspetor"""
    inspections = inspection_service.get_by_inspector(inspector_id)
    return inspections


@router.get(
    "/{inspection_id}/logs",
    response_model=List[InspectionResponse]
)
async def get_logs_by_inspection(
    inspection_id: int,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Busca logs por inspeção"""
    inspections = inspection_service.get_logs_by_inspection(inspection_id)
    return inspections


@router.get("/{inspection_id}", response_model=InspectionResponse)
async def get_inspection(
    inspection_id: int,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Obtém uma inspeção específica por ID"""
    inspection = inspection_service.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspeção não encontrada"
        )
    return inspection


@router.delete("/{inspection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inspection(
    inspection_id: int,
    inspection_service: Session = Depends(get_inspection_service),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma inspeção (não permite se estiver finalizada)"""
    try:
        success = inspection_service.delete(inspection_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inspeção não encontrada"
            )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
