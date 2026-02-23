from typing import List, Optional
from app.mapper import SEVERITY_TO_STATUS
from app.models.inspection import Inspections
from app.schemas.inspection import InspectionUpdate
from app.services.inspections import InspectionService
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.irregularity import Irregularities
from app.schemas.irregularity import (
    IrregularityCreateSchema,
    IrregularityUpdate,
    IrregularityResponse
)


class IrregularityService:
    def __init__(self, db: Session, inspection_service: InspectionService):
        self.db = db
        self.inspection_service = inspection_service

    def create(
        self, irregularity_data: IrregularityCreateSchema
    ) -> IrregularityResponse:
        """Cria uma nova irregularidade"""
        db_irregularity = Irregularities(**irregularity_data.model_dump())
        self.db.add(db_irregularity)

        status = SEVERITY_TO_STATUS[db_irregularity.severity]
        if db_irregularity:
            inspection_update = self.inspection_service.update(
                db_irregularity.inspection_id,
                InspectionUpdate(status=status)
            )
            if not inspection_update or isinstance(inspection_update, ValueError):
                self.db.rollback()
                return inspection_update

        self.db.commit()
        self.db.refresh(db_irregularity)
        return db_irregularity

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[IrregularityResponse]:
        """Lista todas as irregularidades com paginação"""
        stmt = (
            select(Irregularities)
            .offset(skip)
            .limit(limit)
        )
        irregularities = self.db.scalars(stmt).all()
        return irregularities

    def get_by_id(
        self, irregularity_id: int
    ) -> Optional[IrregularityResponse]:
        """Busca uma irregularidade por ID"""
        irregularity = self.db.get(Irregularities, irregularity_id)
        return irregularity

    def get_by_establishment(
        self, establishment_id: int
    ) -> List[IrregularityResponse]:
        """Busca inspeções por estabelecimento"""
        stmt = (
            select(Irregularities)
            .join(Inspections)
            .where(Inspections.establishment_id == establishment_id)
        )
        irregularities = self.db.scalars(stmt).all()
        return irregularities

    def get_by_inspector(
        self, inspector_id: int
    ) -> List[IrregularityResponse]:
        """Busca irregularidades por inspector"""
        stmt = (
            select(Irregularities)
            .where(Irregularities.inspector_id == inspector_id)
        )
        irregularities = self.db.scalars(stmt).all()

        return irregularities

    def update(
        self,
        irregularity_id: int,
        irregularity_data: IrregularityUpdate
    ) -> Optional[IrregularityResponse]:
        """Atualiza uma irregularidade"""
        db_irregularity = self.db.get(Irregularities, irregularity_id)
        if not db_irregularity:
            return None

        update_data = irregularity_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_irregularity, field, value)

        self.db.commit()
        self.db.refresh(db_irregularity)
        return db_irregularity

    def delete(self, irregularity_id: int) -> bool:
        """Deleta uma irregularidade"""
        db_irregularity = self.db.get(Irregularities, irregularity_id)
        if not db_irregularity:
            return False

        self.db.delete(db_irregularity)
        self.db.commit()
        return True
