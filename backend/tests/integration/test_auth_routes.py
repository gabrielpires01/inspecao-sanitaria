"""
Testes de integração para rotas de autenticação
"""
import pytest
from fastapi import status


@pytest.mark.integration
class TestAuthRoutes:
    """Testes para rotas de autenticação"""

    def test_register_success(self, client, sample_user_data):
        """Testa registro de novo usuário via API"""
        response = client.post(
            "/api/auth/register",
            json=sample_user_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "password" not in data

    def test_register_duplicate_email(self, client, sample_user_data):
        """Testa registro com email duplicado via API"""
        response1 = client.post(
            "/api/auth/register",
            json=sample_user_data
        )
        assert response1.status_code == status.HTTP_201_CREATED

        response2 = client.post(
            "/api/auth/register",
            json=sample_user_data
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email já cadastrado" in response2.json()["detail"]

    def test_register_missing_fields(self, client):
        """Testa registro com campos obrigatórios faltando"""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_success(self, client, sample_user, sample_user_data):
        """Testa login com credenciais válidas via API"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_invalid_credentials(self, client, sample_user_data):
        """Testa login com credenciais inválidas via API"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": "senha_incorreta"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email ou senha incorretos" in response.json()["detail"]

    def test_get_current_user_success(self, client, auth_headers):
        """Testa obtenção do usuário atual autenticado"""
        response = client.get(
            "/api/auth/me",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert "id" in data
        assert "password" not in data

    def test_get_current_user_unauthorized(self, client):
        """Testa obtenção do usuário atual sem autenticação"""
        response = client.get("/api/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_invalid_token(self, client):
        """Testa obtenção do usuário atual com token inválido"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer token_invalido"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
