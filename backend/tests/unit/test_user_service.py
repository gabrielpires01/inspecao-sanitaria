import pytest
from app.services.users import UserService
from app.models.user import User
from faker import Faker

fake = Faker("pt_BR")


@pytest.mark.unit
class TestUserService:
    """Testes para UserService"""

    def test_get_users_empty(self, db_session):
        """Testa listagem de usuários quando não há usuários"""
        user_service = UserService(db_session)

        users = user_service.get_users()

        assert users == []
        assert len(users) == 0

    def test_get_users_with_data(self, db_session, sample_user):
        """Testa listagem de usuários com dados"""
        user_service = UserService(db_session)

        users = user_service.get_users()

        assert len(users) == 1
        assert users[0].email == sample_user.email

    def test_get_users_pagination(self, db_session):
        """Testa paginação na listagem de usuários"""
        for _i in range(5):
            user = User(
                email=fake.email(),
                hashed_password="hashed_password",
                full_name=fake.name()
            )
            db_session.add(user)
        db_session.commit()

        user_service = UserService(db_session)

        users_page1 = user_service.get_users(skip=0, limit=2)
        assert len(users_page1) == 2

        users_page2 = user_service.get_users(skip=2, limit=2)
        assert len(users_page2) == 2

        users_page3 = user_service.get_users(skip=4, limit=2)
        assert len(users_page3) == 1

    def test_get_user_by_id_success(self, db_session, sample_user):
        """Testa busca de usuário por ID com sucesso"""
        user_service = UserService(db_session)

        user = user_service.get_user(sample_user.id)

        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email

    def test_get_user_by_id_not_found(self, db_session):
        """Testa busca de usuário por ID inexistente"""
        user_service = UserService(db_session)

        user = user_service.get_user(99999)

        assert user is None
