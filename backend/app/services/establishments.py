from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inspection import Establishments
from app.schemas.establishment import (
    EstablishmentCreate,
    EstablishmentUpdate,
    EstablishmentResponse
)


class EstablishmentService:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, establishment_data: EstablishmentCreate
    ) -> EstablishmentResponse:
        """Cria um novo estabelecimento"""
        db_establishment = Establishments(**establishment_data.model_dump(exclude={'id'}))
        self.db.add(db_establishment)
        self.db.commit()
        self.db.refresh(db_establishment)
        return db_establishment

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[EstablishmentResponse]:
        """Lista todos os estabelecimentos com paginação"""
        establishments = (
            self.db.query(Establishments)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return establishments

    def get_by_id(
        self, establishment_id: int
    ) -> Optional[EstablishmentResponse]:
        """Busca um estabelecimento por ID"""
        establishment = self.db.get(Establishments, establishment_id)
        return establishment

    def update(
        self,
        establishment_id: int,
        establishment_data: EstablishmentUpdate
    ) -> Optional[EstablishmentResponse]:
        """Atualiza um estabelecimento"""
        db_establishment = self.db.get(Establishments, establishment_id)
        if not db_establishment:
            return None

        update_data = establishment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_establishment, field, value)

        self.db.commit()
        self.db.refresh(db_establishment)
        return db_establishment

    def delete(self, establishment_id: int) -> bool:
        """Deleta um estabelecimento"""
        db_establishment = self.db.get(Establishments, establishment_id)
        if not db_establishment:
            return False

        self.db.delete(db_establishment)
        self.db.commit()
        return True

    def search_by_name(self, name: str) -> List[EstablishmentResponse]:
        """Busca estabelecimentos por nome (busca parcial)"""
        establishments = (
            self.db.query(Establishments)
            .filter(Establishments.name.ilike(f"%{name}%"))
            .all()
        )
        return establishments
