import pytest
from fastapi import status


@pytest.mark.integration
class TestEstablishmentRoutes:
    """Testes para rotas de estabelecimentos"""

    def test_create_establishment_success(self, client, auth_headers, sample_establishment_data):
        """Testa criação de estabelecimento via API"""
        response = client.post(
            "/api/establishments/",
            json=sample_establishment_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_establishment_data["name"]
        assert "id" in data

    def test_create_establishment_unauthorized(self, client, sample_establishment_data):
        """Testa criação sem autenticação"""
        response = client.post(
            "/api/establishments/",
            json=sample_establishment_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_establishments_success(self, client, auth_headers, sample_establishment):
        """Testa listagem de estabelecimentos"""
        response = client.get(
            "/api/establishments/",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_establishments_unauthorized(self, client):
        """Testa listagem sem autenticação"""
        response = client.get("/api/establishments/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_establishment_by_id_success(self, client, auth_headers, sample_establishment):
        """Testa busca de estabelecimento por ID"""
        response = client.get(
            f"/api/establishments/{sample_establishment.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_establishment.id
        assert data["name"] == sample_establishment.name

    def test_get_establishment_by_id_not_found(self, client, auth_headers):
        """Testa busca de estabelecimento inexistente"""
        response = client.get(
            "/api/establishments/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_establishment_success(self, client, auth_headers, sample_establishment):
        """Testa atualização de estabelecimento"""
        update_data = {"name": "Nome Atualizado"}

        response = client.put(
            f"/api/establishments/{sample_establishment.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Nome Atualizado"

    def test_delete_establishment_success(self, client, auth_headers, sample_establishment):
        """Testa deleção de estabelecimento"""
        response = client.delete(
            f"/api/establishments/{sample_establishment.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_search_establishments_success(self, client, auth_headers, sample_establishment):
        """Testa busca de estabelecimentos por nome"""
        response = client.get(
            f"/api/establishments/search?name={sample_establishment.name[:5]}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
