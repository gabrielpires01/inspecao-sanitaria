"""
Testes unitários para funções de segurança
"""
import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)
from fastapi import HTTPException, status


@pytest.mark.unit
class TestSecurity:
    """Testes para funções de segurança"""

    def test_get_password_hash(self):
        """Testa hash de senha"""
        password = "MinhaSenha123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > 0
        assert isinstance(hashed, str)

    def test_verify_password_correct(self):
        """Testa verificação de senha correta"""
        password = "MinhaSenha123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta"""
        password = "MinhaSenha123"
        wrong_password = "SenhaErrada456"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    def test_create_access_token(self):
        """Testa criação de token de acesso"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Testa verificação de token válido"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

        email = verify_token(token, credentials_exception)
        assert email == "test@example.com"

    def test_verify_token_invalid(self):
        """Testa verificação de token inválido"""
        invalid_token = "token.invalido.aqui"

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

        with pytest.raises(HTTPException) as exc_info:
            verify_token(invalid_token, credentials_exception)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
