import pytest
from app.services.establishments import EstablishmentService
from app.schemas.establishment import EstablishmentCreate, EstablishmentUpdate
from app.models.inspection import Establishments
from faker import Faker

fake = Faker("pt_BR")


@pytest.mark.unit
class TestEstablishmentService:
    """Testes para EstablishmentService"""

    def test_create_success(self, db_session, sample_establishment_data):
        """Testa criação de estabelecimento com sucesso"""
        service = EstablishmentService(db_session)
        establishment_data = EstablishmentCreate(**sample_establishment_data)

        result = service.create(establishment_data)

        assert result is not None
        assert result.name == sample_establishment_data["name"]
        assert result.address == sample_establishment_data["address"]

    def test_get_all_empty(self, db_session):
        """Testa listagem quando não há estabelecimentos"""
        service = EstablishmentService(db_session)

        establishments = service.get_all()

        assert establishments == []

    def test_get_all_with_data(self, db_session, sample_establishment):
        """Testa listagem de estabelecimentos com dados"""
        service = EstablishmentService(db_session)

        establishments = service.get_all()

        assert len(establishments) == 1
        assert establishments[0].name == sample_establishment.name

    def test_get_all_pagination(self, db_session):
        """Testa paginação na listagem"""
        for _i in range(5):
            establishment = Establishments(
                name=fake.company(),
                address=fake.address(),
                city=fake.city()
            )
            db_session.add(establishment)
        db_session.commit()

        service = EstablishmentService(db_session)

        page1 = service.get_all(skip=0, limit=2)
        assert len(page1) == 2

        page2 = service.get_all(skip=2, limit=2)
        assert len(page2) == 2

    def test_get_by_id_success(self, db_session, sample_establishment):
        """Testa busca por ID com sucesso"""
        service = EstablishmentService(db_session)

        result = service.get_by_id(sample_establishment.id)

        assert result is not None
        assert result.id == sample_establishment.id

    def test_get_by_id_not_found(self, db_session):
        """Testa busca por ID inexistente"""
        service = EstablishmentService(db_session)

        result = service.get_by_id(99999)

        assert result is None

    def test_update_success(self, db_session, sample_establishment):
        """Testa atualização de estabelecimento"""
        service = EstablishmentService(db_session)
        update_data = EstablishmentUpdate(name="Nome Atualizado")

        result = service.update(sample_establishment.id, update_data)

        assert result is not None
        assert result.name == "Nome Atualizado"
        assert result.id == sample_establishment.id

    def test_update_not_found(self, db_session):
        """Testa atualização de estabelecimento inexistente"""
        service = EstablishmentService(db_session)
        update_data = EstablishmentUpdate(name="Nome Atualizado")

        result = service.update(99999, update_data)

        assert result is None

    def test_delete_success(self, db_session, sample_establishment):
        """Testa deleção de estabelecimento"""
        service = EstablishmentService(db_session)

        result = service.delete(sample_establishment.id)

        assert result is True
        assert service.get_by_id(sample_establishment.id) is None

    def test_delete_not_found(self, db_session):
        """Testa deleção de estabelecimento inexistente"""
        service = EstablishmentService(db_session)

        result = service.delete(99999)

        assert result is False

    def test_search_by_name(self, db_session):
        """Testa busca por nome"""
        establishment1 = Establishments(name="Restaurante Bom Sabor")
        establishment2 = Establishments(name="Padaria Doce Manhã")
        establishment3 = Establishments(name="Supermercado Central")
        db_session.add_all([establishment1, establishment2, establishment3])
        db_session.commit()

        service = EstablishmentService(db_session)

        results = service.search_by_name("Restaurante")

        assert len(results) == 1
        assert results[0].name == "Restaurante Bom Sabor"
