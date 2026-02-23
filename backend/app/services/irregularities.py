from typing import List, Optional
from app.enums import Status
from app.models.inspection import Inspections
from app.schemas.inspection import InspectionUpdate
from app.services.inspections import InspectionService
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.irregularity import Irregularities, IrregularitiesLog
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
        db_irregularity = Irregularities(**irregularity_data.model_dump(exclude={'id'}))
        self.db.add(db_irregularity)

        if db_irregularity:
            inspection_update = self._update_inspection(db_irregularity)
            if not inspection_update or isinstance(inspection_update, ValueError):
                self.db.rollback()
                return inspection_update

        self.db.commit()
        self.db.refresh(db_irregularity)
        return db_irregularity

    def _update_inspection(self, irregularity: Irregularities) -> Inspections:
        requires_interruption = irregularity.requires_interruption
        status = Status.has_irregularities
        if requires_interruption:
            status = Status.immediate_prohibition

        inspection_update = self.inspection_service.update(
            irregularity.inspection_id,
            InspectionUpdate(status=status)
        )
        return inspection_update

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

    def get_all_logs_by_irregularity(
            self, irregularity_id: int, skip: int = 0, limit: int = 100
    ) -> List[IrregularityResponse]:
        """Lista todas os logs de uma irregularidades com paginação"""
        stmt = (
            select(IrregularitiesLog)
            .where(IrregularitiesLog.irregularity_id == irregularity_id)
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

    def get_by_inspection(
        self, inspection_id: int
    ) -> List[IrregularityResponse]:
        """Busca irregularidades por inspeção"""
        stmt = (
            select(Irregularities)
            .where(Irregularities.inspection_id == inspection_id)
        )
        irregularities = self.db.scalars(stmt).all()
        return irregularities

    def update(
        self,
        irregularity_id: int,
        irregularity_data: IrregularityUpdate
    ) -> Optional[IrregularityResponse | ValueError]:
        """Atualiza uma irregularidade"""
        db_irregularity = self.db.get(Irregularities, irregularity_id)
        if not db_irregularity:
            return None

        inspection = self.db.get(Inspections, db_irregularity.inspection_id)
        if inspection and self.inspection_service.is_finalized(inspection.status):
            raise ValueError(
                "Não é permitido alterar após a inspeção ser finalizada"
            )

        update_data = irregularity_data.model_dump(exclude_unset=True)
        old_severity = db_irregularity.severity
        new_severity = update_data["severity"]
        for field, value in update_data.items():
            setattr(db_irregularity, field, value)

        irregularity_log = IrregularitiesLog(
            irregularity_id=irregularity_id,
            inspector_id=db_irregularity.inspector_id,
            new_severity=new_severity,
            old_severity=old_severity
        )

        self.db.add(irregularity_log)
        self.db.commit()
        self.db.refresh(db_irregularity)
        self.db.refresh(irregularity_log)

        self._update_inspection(db_irregularity)

        return db_irregularity

    def delete(self, irregularity_id: int) -> bool:
        """Deleta uma irregularidade"""
        db_irregularity = self.db.get(Irregularities, irregularity_id)
        if not db_irregularity:
            return False

        self.db.delete(db_irregularity)
        self.db.commit()
        return True
