import pytest
from app.services.auth import AuthService
from app.schemas.user import UserCreate


@pytest.mark.unit
class TestAuthService:
    """Testes para AuthService"""

    def test_register_success(self, db_session, sample_user_data):
        """Testa registro de novo usuário com sucesso"""
        auth_service = AuthService(db_session)
        user_data = UserCreate(**sample_user_data)

        result = auth_service.register(user_data)

        assert result is not None
        assert result.email == sample_user_data["email"]
        assert result.full_name == sample_user_data["full_name"]
        assert result.hashed_password != sample_user_data["password"]

    def test_register_duplicate_email(self, db_session, sample_user_data):
        """Testa registro com email já existente"""
        auth_service = AuthService(db_session)
        user_data = UserCreate(**sample_user_data)

        first_result = auth_service.register(user_data)
        assert first_result is not None

        duplicate_result = auth_service.register(user_data)
        assert duplicate_result is None

    def test_login_success(self, db_session, sample_user, sample_user_data):
        """Testa login com credenciais válidas"""
        from unittest.mock import MagicMock

        auth_service = AuthService(db_session)

        login_data = MagicMock()
        login_data.email = sample_user_data["email"]
        login_data.password = sample_user_data["password"]
        result = auth_service.login(login_data)

        assert result is not None
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        assert len(result["access_token"]) > 0

    def test_login_invalid_email(self, db_session, sample_user_data):
        """Testa login com email inválido"""
        from unittest.mock import MagicMock

        auth_service = AuthService(db_session)
        login_data = MagicMock()
        login_data.email = "email_inexistente@teste.com"
        login_data.password = sample_user_data["password"]

        result = auth_service.login(login_data)

        assert result is None

    def test_login_invalid_password(self, db_session, sample_user, sample_user_data):
        """Testa login com senha inválida"""
        from unittest.mock import MagicMock

        auth_service = AuthService(db_session)
        login_data = MagicMock()
        login_data.email = sample_user_data["email"]
        login_data.password = "senha_incorreta"

        result = auth_service.login(login_data)

        assert result is None
