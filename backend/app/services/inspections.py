from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.inspection import FinalizationLog, InspectionLog, Inspections
from app.enums import Status, FinalizeStatus
from app.schemas.inspection import (
    FinalizeInspectionService,
    InspectionCreateService,
    InspectionUpdate,
    InspectionResponse
)


class InspectionService:
    def __init__(self, db: Session):
        self.db = db

    def is_finalized(self, status: Status) -> bool:
        """Verifica se o status indica que a inspeção está finalizada"""
        finalized_statuses = [
            Status.finalized,
            Status.finalized_prohibition,
            Status.finalized_partial_prohibition
        ]
        return status in finalized_statuses

    def create(
        self, inspection_data: InspectionCreateService
    ) -> InspectionResponse:
        """Cria uma nova inspeção"""
        db_inspection = Inspections(**inspection_data.model_dump(exclude={'id'}))
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
        stmt = (
            select(Inspections)
            .where(Inspections.establishment_id == establishment_id)
        )
        inspections = self.db.scalars(stmt).all()
        return inspections

    def get_by_inspector(
        self, inspector_id: int
    ) -> List[InspectionResponse]:
        """Busca inspeções por inspetor"""
        stmt = (
            select(Inspections)
            .where(Inspections.inspector_id == inspector_id)
        )
        inspections = self.db.scalars(stmt).all()
        return inspections

    def update(
        self,
        inspection_id: int,
        inspection_data: InspectionUpdate
    ) -> Optional[InspectionResponse | ValueError]:
        """Atualiza uma inspeção (não permite se estiver finalizada)"""
        db_inspection = self.db.get(Inspections, inspection_id)
        if not db_inspection:
            return None

        if self.is_finalized(db_inspection.status):
            return ValueError(
                "Não é permitido alterar inspeções finalizadas"
            )

        old_status = db_inspection.status
        new_status = inspection_data.status
        update_data = inspection_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inspection, field, value)

        log = None
        if new_status:
            log = self.add_update_log(db_inspection.inspector_id, inspection_id, old_status, new_status)

        self.db.commit()
        self.db.refresh(db_inspection)
        if log:
            self.db.refresh(log)

        return db_inspection

    def delete(self, inspection_id: int) -> bool:
        """Deleta uma inspeção (não permite se estiver finalizada)"""
        db_inspection = self.db.get(Inspections, inspection_id)
        if not db_inspection:
            return False

        if self.i | ValueErrors_finalized(db_inspection.status):
            raise ValueError(
                "Não é permitido deletar inspeções finalizadas"
            )

        self.db.delete(db_inspection)
        self.db.commit()
        return True

    def add_update_log(self, inspector_id, inspection_id, old_status, new_status) -> InspectionLog:
        """Atualiza log da inspeção"""
        update_log = InspectionLog(**{
            "old_status": old_status,
            "new_status": new_status,
            "inspection_id": inspection_id,
            "inspector_id": inspector_id
        })

        self.db.add(update_log)
        return update_log

    def get_logs_by_inspection(self, inspection_id) -> List[InspectionLog]:
        """Busca logs de inspeção por inspeção"""
        stmt = (
            select(InspectionLog)
            .where(InspectionLog.inspection_id == inspection_id)
        )

        logs = self.db.scalars(stmt).all()
        return logs

    def finalize_inspection(self, finalization_data: FinalizeInspectionService):
        """Finaliza uma inspeção"""
        log = FinalizationLog(**finalization_data.model_dump(exclude={'id'}))

        self.db.add(log)
        status = Status.finalized
        if log.status == FinalizeStatus.partial_prohibition:
            status = Status.finalized_partial_prohibition
        elif log.status == FinalizeStatus.prohibition:
            status = Status.finalized_prohibition

        self.update(log.inspection_id, InspectionUpdate(status=status))

        self.db.commit()
        self.db.refresh(log)
        return log

    def get_finalization_logs_by_inspection(self, inspection_id: int) -> List[FinalizationLog]:
        """Busca logs de finalização por inspeção"""
        stmt = (
            select(FinalizationLog)
            .where(FinalizationLog.inspection_id == inspection_id)
        )

        logs = self.db.scalars(stmt).all()
        return logs
