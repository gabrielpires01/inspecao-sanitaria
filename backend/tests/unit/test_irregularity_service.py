import pytest
from app.services.irregularities import IrregularityService
from app.services.inspections import InspectionService
from app.schemas.irregularity import IrregularityCreateSchema, IrregularityUpdate
from app.models.irregularity import Irregularities
from app.enums import Severity


@pytest.mark.unit
class TestIrregularityService:
    """Testes para IrregularityService"""

    def test_create_success(self, db_session, sample_inspection, sample_user):
        """Testa criação de irregularidade com sucesso"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularity_data = IrregularityCreateSchema(
            inspection_id=sample_inspection.id,
            inspector_id=sample_user.id,
            description="Teste de irregularidade",
            severity=Severity.moderate,
            requires_interruption=False
        )

        result = service.create(irregularity_data)

        assert result is not None
        assert result.inspection_id == sample_inspection.id
        assert result.description == "Teste de irregularidade"

    def test_get_all_empty(self, db_session):
        """Testa listagem quando não há irregularidades"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularities = service.get_all()

        assert irregularities == []

    def test_get_all_with_data(self, db_session, sample_inspection, sample_user):
        """Testa listagem de irregularidades com dados"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularity = Irregularities(
            inspection_id=sample_inspection.id,
            inspector_id=sample_user.id,
            description="Teste",
            severity=Severity.moderate,
            requires_interruption=False
        )
        db_session.add(irregularity)
        db_session.commit()

        irregularities = service.get_all()

        assert len(irregularities) == 1
        assert irregularities[0].description == "Teste"

    def test_get_by_id_success(self, db_session, sample_inspection, sample_user):
        """Testa busca por ID com sucesso"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularity = Irregularities(
            inspection_id=sample_inspection.id,
            inspector_id=sample_user.id,
            description="Teste",
            severity=Severity.moderate,
            requires_interruption=False
        )
        db_session.add(irregularity)
        db_session.commit()
        db_session.refresh(irregularity)

        result = service.get_by_id(irregularity.id)

        assert result is not None
        assert result.id == irregularity.id

    def test_get_by_id_not_found(self, db_session):
        """Testa busca por ID inexistente"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        result = service.get_by_id(99999)

        assert result is None

    def test_get_by_inspection(self, db_session, sample_inspection, sample_user):
        """Testa busca por inspeção"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        for _i in range(3):
            irregularity = Irregularities(
                inspection_id=sample_inspection.id,
                inspector_id=sample_user.id,
                description=f"Irregularidade {_i}",
                severity=Severity.moderate,
                requires_interruption=False
            )
            db_session.add(irregularity)
        db_session.commit()

        results = service.get_by_inspection(sample_inspection.id)

        assert len(results) == 3
        assert all(r.inspection_id == sample_inspection.id for r in results)

    def test_update_success(self, db_session, sample_inspection, sample_user):
        """Testa atualização de irregularidade"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularity = Irregularities(
            inspection_id=sample_inspection.id,
            inspector_id=sample_user.id,
            description="Original",
            severity=Severity.moderate,
            requires_interruption=False
        )
        db_session.add(irregularity)
        db_session.commit()
        db_session.refresh(irregularity)

        update_data = IrregularityUpdate(description="Atualizada", severity=Severity.major)
        result = service.update(irregularity.id, update_data)

        assert result is not None
        assert result.description == "Atualizada"
        assert result.severity == Severity.major

    def test_update_not_found(self, db_session):
        """Testa atualização de irregularidade inexistente"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)
        update_data = IrregularityUpdate(description="Atualizada")

        result = service.update(99999, update_data)

        assert result is None

    def test_delete_success(self, db_session, sample_inspection, sample_user):
        """Testa deleção de irregularidade"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        irregularity = Irregularities(
            inspection_id=sample_inspection.id,
            inspector_id=sample_user.id,
            description="Teste",
            severity=Severity.moderate,
            requires_interruption=False
        )
        db_session.add(irregularity)
        db_session.commit()
        db_session.refresh(irregularity)

        result = service.delete(irregularity.id)

        assert result is True
        assert service.get_by_id(irregularity.id) is None

    def test_delete_not_found(self, db_session):
        """Testa deleção de irregularidade inexistente"""
        inspection_service = InspectionService(db_session)
        service = IrregularityService(db_session, inspection_service)

        result = service.delete(99999)

        assert result is False
