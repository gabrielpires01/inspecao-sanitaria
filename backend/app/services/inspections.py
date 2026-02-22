from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inspection import Inspections
from app.enums import Status
from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse
)


class InspectionService:
    def __init__(self, db: Session):
        self.db = db

    def _is_finalized(self, status: Status) -> bool:
        """Verifica se o status indica que a inspeção está finalizada"""
        finalized_statuses = [
            Status.finalized,
            Status.finalized_prohibition,
            Status.finalized_partial_prohibition
        ]
        return status in finalized_statuses

    def create(
        self, inspection_data: InspectionCreate
    ) -> InspectionResponse:
        """Cria uma nova inspeção"""
        db_inspection = Inspections(**inspection_data.model_dump())
        self.db.add(db_inspection)
        self.db.commit()
        self.db.refresh(db_inspection)
        return db_inspection

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[InspectionResponse]:
        """Lista todas as inspeções com paginação"""
        inspections = (
            self.db.query(Inspections)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return inspections

    def get_by_id(
        self, inspection_id: int
    ) -> Optional[InspectionResponse]:
        """Busca uma inspeção por ID"""
        inspection = self.db.get(Inspections, inspection_id)
        return inspection

    def get_by_establishment(
        self, establishment_id: int
    ) -> List[InspectionResponse]:
        """Busca inspeções por estabelecimento"""
        inspections = (
            self.db.query(Inspections)
            .filter(Inspections.establishment_id == establishment_id)
            .all()
        )
        return inspections

    def get_by_inspector(
        self, inspector_id: int
    ) -> List[InspectionResponse]:
        """Busca inspeções por inspetor"""
        inspections = (
            self.db.query(Inspections)
            .filter(Inspections.inspector_id == inspector_id)
            .all()
        )
        return inspections

    def update(
        self,
        inspection_id: int,
        inspection_data: InspectionUpdate
    ) -> Optional[InspectionResponse]:
        """Atualiza uma inspeção (não permite se estiver finalizada)"""
        db_inspection = self.db.get(Inspections, inspection_id)
        if not db_inspection:
            return None

        if self._is_finalized(db_inspection.status):
            return ValueError(
                "Não é permitido alterar inspeções finalizadas"
            )

        update_data = inspection_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inspection, field, value)

        self.db.commit()
        self.db.refresh(db_inspection)
        return db_inspection

    def delete(self, inspection_id: int) -> bool:
        """Deleta uma inspeção (não permite se estiver finalizada)"""
        db_inspection = self.db.get(Inspections, inspection_id)
        if not db_inspection:
            return False

        if self._is_finalized(db_inspection.status):
            raise ValueError(
                "Não é permitido deletar inspeções finalizadas"
            )

        self.db.delete(db_inspection)
        self.db.commit()
        return True
