import pytest
from app.services.inspections import InspectionService
from app.schemas.inspection import InspectionCreateService, InspectionUpdate
from app.models.inspection import Inspections
from app.enums import Status


@pytest.mark.unit
class TestInspectionService:
    """Testes para InspectionService"""

    def test_create_success(self, db_session, sample_establishment, sample_user):
        """Testa criação de inspeção com sucesso"""
        service = InspectionService(db_session)
        inspection_data = InspectionCreateService(
            establishment_id=sample_establishment.id,
            inspector_id=sample_user.id,
            status=Status.clear
        )

        result = service.create(inspection_data)

        assert result is not None
        assert result.establishment_id == sample_establishment.id
        assert result.inspector_id == sample_user.id

    def test_get_all_empty(self, db_session):
        """Testa listagem quando não há inspeções"""
        service = InspectionService(db_session)

        inspections = service.get_all()

        assert inspections == []

    def test_get_all_with_data(self, db_session, sample_inspection):
        """Testa listagem de inspeções com dados"""
        service = InspectionService(db_session)

        inspections = service.get_all()

        assert len(inspections) == 1
        assert inspections[0].id == sample_inspection.id

    def test_get_by_id_success(self, db_session, sample_inspection):
        """Testa busca por ID com sucesso"""
        service = InspectionService(db_session)

        result = service.get_by_id(sample_inspection.id)

        assert result is not None
        assert result.id == sample_inspection.id

    def test_get_by_id_not_found(self, db_session):
        """Testa busca por ID inexistente"""
        service = InspectionService(db_session)

        result = service.get_by_id(99999)

        assert result is None

    def test_get_by_establishment(self, db_session, sample_establishment, sample_user):
        """Testa busca por estabelecimento"""
        service = InspectionService(db_session)

        for _i in range(3):
            inspection = Inspections(
                establishment_id=sample_establishment.id,
                inspector_id=sample_user.id,
                status=Status.clear
            )
            db_session.add(inspection)
        db_session.commit()

        results = service.get_by_establishment(sample_establishment.id)

        assert len(results) == 3
        assert all(r.establishment_id == sample_establishment.id for r in results)

    def test_get_by_inspector(self, db_session, sample_establishment, sample_user):
        """Testa busca por inspetor"""
        service = InspectionService(db_session)

        for _i in range(2):
            inspection = Inspections(
                establishment_id=sample_establishment.id,
                inspector_id=sample_user.id,
                status=Status.clear
            )
            db_session.add(inspection)
        db_session.commit()

        results = service.get_by_inspector(sample_user.id)

        assert len(results) >= 2
        assert all(r.inspector_id == sample_user.id for r in results)

    def test_update_success(self, db_session, sample_inspection):
        """Testa atualização de inspeção"""
        service = InspectionService(db_session)
        update_data = InspectionUpdate(status=Status.has_irregularities)

        result = service.update(sample_inspection.id, update_data)

        assert result is not None
        assert result.status == Status.has_irregularities

    def test_update_not_found(self, db_session):
        """Testa atualização de inspeção inexistente"""
        service = InspectionService(db_session)
        update_data = InspectionUpdate(status=Status.has_irregularities)

        result = service.update(99999, update_data)

        assert result is None

    def test_delete_success(self, db_session, sample_inspection):
        """Testa deleção de inspeção"""
        service = InspectionService(db_session)

        result = service.delete(sample_inspection.id)

        assert result is True
        assert service.get_by_id(sample_inspection.id) is None

    def test_delete_not_found(self, db_session):
        """Testa deleção de inspeção inexistente"""
        service = InspectionService(db_session)

        result = service.delete(99999)

        assert result is False
