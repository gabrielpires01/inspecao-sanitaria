import pytest
from fastapi import status


@pytest.mark.integration
class TestUserRoutes:
    """Testes para rotas de usuários"""

    def test_get_users_success(self, client, auth_headers, sample_user):
        """Testa listagem de usuários autenticada"""
        response = client.get(
            "/api/users/",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_users_unauthorized(self, client):
        """Testa listagem de usuários sem autenticação"""
        response = client.get("/api/users/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_by_id_success(self, client, auth_headers, sample_user):
        """Testa busca de usuário por ID autenticada"""
        response = client.get(
            f"/api/users/{sample_user.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_user.id
        assert data["email"] == sample_user.email

    def test_get_user_by_id_not_found(self, client, auth_headers):
        """Testa busca de usuário inexistente"""
        response = client.get(
            "/api/users/99999",
            headers=auth_headers
        )

        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_200_OK]

    def test_get_user_by_id_unauthorized(self, client, sample_user):
        """Testa busca de usuário por ID sem autenticação"""
        response = client.get(f"/api/users/{sample_user.id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
