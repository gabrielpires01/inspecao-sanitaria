import pytest
from fastapi import status
from app.enums import Severity


@pytest.mark.integration
class TestIrregularityRoutes:
    """Testes para rotas de irregularidades"""

    def test_create_irregularity_success(self, client, auth_headers, sample_inspection):
        """Testa criação de irregularidade via API"""
        irregularity_data = {
            "inspection_id": sample_inspection.id,
            "description": "Teste de irregularidade",
            "severity": Severity.moderate,
            "requires_interruption": False
        }

        response = client.post(
            "/api/irregularities/",
            json=irregularity_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["inspection_id"] == sample_inspection.id
        assert data["description"] == "Teste de irregularidade"
        assert "id" in data

    def test_create_irregularity_unauthorized(self, client, sample_inspection):
        """Testa criação sem autenticação"""
        irregularity_data = {
            "inspection_id": sample_inspection.id,
            "description": "Teste",
            "severity": Severity.moderate
        }

        response = client.post(
            "/api/irregularities/",
            json=irregularity_data
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_irregularities_success(self, client, auth_headers):
        """Testa listagem de irregularidades"""
        response = client.get(
            "/api/irregularities/",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_irregularities_unauthorized(self, client):
        """Testa listagem sem autenticação"""
        response = client.get("/api/irregularities/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_irregularity_by_id_success(
        self, client, auth_headers, sample_inspection, sample_user
    ):
        """Testa busca de irregularidade por ID"""
        irregularity_data = {
            "inspection_id": sample_inspection.id,
            "description": "Teste",
            "severity": Severity.moderate,
            "requires_interruption": False
        }
        
        create_response = client.post(
            "/api/irregularities/",
            json=irregularity_data,
            headers=auth_headers
        )
        irregularity_id = create_response.json()["id"]

        response = client.get(
            f"/api/irregularities/{irregularity_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == irregularity_id

    def test_get_irregularity_by_id_not_found(self, client, auth_headers):
        """Testa busca de irregularidade inexistente"""
        response = client.get(
            "/api/irregularities/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_irregularities_by_inspection(self, client, auth_headers, sample_inspection):
        """Testa busca de irregularidades por inspeção"""
        response = client.get(
            f"/api/irregularities/inspection/{sample_inspection.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_update_irregularity_success(self, client, auth_headers, sample_inspection):
        """Testa atualização de irregularidade"""
        create_data = {
            "inspection_id": sample_inspection.id,
            "description": "Original",
            "severity": Severity.moderate,
            "requires_interruption": False
        }
        create_response = client.post(
            "/api/irregularities/",
            json=create_data,
            headers=auth_headers
        )
        irregularity_id = create_response.json()["id"]

        update_data = {
            "description": "Atualizada",
            "severity": Severity.major
        }
        response = client.put(
            f"/api/irregularities/{irregularity_id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == "Atualizada"

    def test_update_irregularity_finalized(self, client, auth_headers, sample_finalized_inspection):
        """Testa atualização de irregularidade finalizada"""
        update_data = {
            "severity": Severity.major
        }
        response = client.put(
            f"/api/irregularities/{sample_finalized_inspection.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Não é permitido alterar após a inspeção ser finalizada" in response.json()["detail"]

    def test_delete_irregularity_success(self, client, auth_headers, sample_inspection):
        """Testa deleção de irregularidade"""
        create_data = {
            "inspection_id": sample_inspection.id,
            "description": "Para deletar",
            "severity": Severity.moderate,
            "requires_interruption": False
        }
        create_response = client.post(
            "/api/irregularities/",
            json=create_data,
            headers=auth_headers
        )
        irregularity_id = create_response.json()["id"]

        response = client.delete(
            f"/api/irregularities/{irregularity_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
