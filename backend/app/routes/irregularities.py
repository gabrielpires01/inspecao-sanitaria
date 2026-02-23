from typing import List
from app.enums import Severity
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.core.deps import get_irregularity_service
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.irregularity import (
    IrregularityCreate,
    IrregularityCreateSchema,
    IrregularityUpdate,
    IrregularityUpdateSchema,
    IrregularityResponse,
    IrregularityResolve,
    IrregularityLogsResponse
)

router = APIRouter()


@router.post(
    "/",
    response_model=IrregularityResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_irregularity(
    irregularity_data: IrregularityCreate,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova irregularidade"""
    dict_data = dict(irregularity_data)

    irregularity_data = irregularity_service.create(IrregularityCreateSchema(
        **dict_data,
        inspector_id=current_user.id
    ))

    return irregularity_data


@router.get("/", response_model=List[IrregularityResponse])
async def list_irregularities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as irregularidades com paginação"""
    irregularities = irregularity_service.get_all(skip=skip, limit=limit)
    return irregularities


@router.get("/logs/{irregularity_id}", response_model=List[IrregularityLogsResponse])
async def list_irregularity_logs(
    irregularity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as irregularidades com paginação"""
    irregularities = irregularity_service.get_all_logs_by_irregularity(
        irregularity_id=irregularity_id,
        skip=skip,
        limit=limit
    )
    return irregularities


@router.get(
    "/establishment/{establishment_id}",
    response_model=List[IrregularityResponse]
)
async def get_irregularities_by_establishment(
    establishment_id: int,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Busca irregularidades por estabelecimento"""
    irregularities = irregularity_service.get_by_establishment(establishment_id)
    return irregularities


@router.get(
    "/inspector/{inspector_id}",
    response_model=List[IrregularityResponse]
)
async def get_irregularities_by_inspector(
    inspector_id: int,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Busca irregularidades por inspetor"""
    irregularities = irregularity_service.get_by_inspector(inspector_id)
    return irregularities


@router.get(
    "/inspection/{inspection_id}",
    response_model=List[IrregularityResponse]
)
async def get_irregularities_by_inspection(
    inspection_id: int,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Busca irregularidades por inspeção"""
    irregularities = irregularity_service.get_by_inspection(inspection_id)
    return irregularities


@router.get("/{irregularity_id}", response_model=IrregularityResponse)
async def get_irregularity(
    irregularity_id: int,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Obtém uma irregularidade específica por ID"""
    irregularity = irregularity_service.get_by_id(irregularity_id)
    if not irregularity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inspeção não encontrada"
        )
    return irregularity


@router.put("/{irregularity_id}", response_model=IrregularityResponse)
async def update_irregularity(
    irregularity_id: int,
    irregularity_data: IrregularityUpdate,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma irregularidade"""
    try:
        dict_data = dict(irregularity_data)
        irregularity = irregularity_service.update(
            irregularity_id, IrregularityUpdateSchema(
                **dict_data,
                inspector_id=current_user.id
            )
        )
        if not irregularity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Irregularidade não encontrada"
            )
        return irregularity
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/resolve/{irregularity_id}", response_model=IrregularityResponse)
async def resolve_irregularity(
    irregularity_id: int,
    irregularity_data: IrregularityResolve,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Resolve irregularida"""
    try:
        dict_data = dict(irregularity_data)
        irregularity = irregularity_service.update(
            irregularity_id, IrregularityUpdateSchema(
                **dict_data,
                inspector_id=current_user.id,
                severity=Severity.resolved
            )
        )
        if not irregularity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Irregularidade não encontrada"
            )
        return irregularity
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{irregularity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_irregularity(
    irregularity_id: int,
    irregularity_service: Session = Depends(get_irregularity_service),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma irregularidade"""
    try:
        success = irregularity_service.delete(irregularity_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Irregularidade não encontrada"
            )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
