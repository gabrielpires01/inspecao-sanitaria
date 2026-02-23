"""
Testes de integração para rotas de inspeções
"""
import pytest
from fastapi import status
from app.enums import Status


@pytest.mark.integration
class TestInspectionRoutes:
    """Testes para rotas de inspeções"""

    def test_create_inspection_success(self, client, auth_headers, sample_establishment):
        """Testa criação de inspeção via API"""
        inspection_data = {
            "establishment_id": sample_establishment.id,
            "status": Status.clear
        }

        response = client.post(
            "/api/inspections/",
            json=inspection_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["establishment_id"] == sample_establishment.id
        assert "id" in data

    def test_create_inspection_unauthorized(self, client, sample_establishment):
        """Testa criação sem autenticação"""
        inspection_data = {
            "establishment_id": sample_establishment.id,
            "status": Status.clear
        }

        response = client.post(
            "/api/inspections/",
            json=inspection_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_inspections_success(self, client, auth_headers, sample_inspection):
        """Testa listagem de inspeções"""
        response = client.get(
            "/api/inspections/",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_list_inspections_unauthorized(self, client):
        """Testa listagem sem autenticação"""
        response = client.get("/api/inspections/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_inspection_by_id_success(self, client, auth_headers, sample_inspection):
        """Testa busca de inspeção por ID"""
        response = client.get(
            f"/api/inspections/{sample_inspection.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_inspection.id

    def test_get_inspection_by_id_not_found(self, client, auth_headers):
        """Testa busca de inspeção inexistente"""
        response = client.get(
            "/api/inspections/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_inspections_by_establishment(self, client, auth_headers, sample_establishment, sample_inspection):
        """Testa busca de inspeções por estabelecimento"""
        response = client.get(
            f"/api/inspections/establishment/{sample_establishment.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_inspections_by_inspector(self, client, auth_headers, sample_user, sample_inspection):
        """Testa busca de inspeções por inspetor"""
        response = client.get(
            f"/api/inspections/inspector/{sample_user.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)