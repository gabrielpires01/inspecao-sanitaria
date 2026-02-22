"""
Testes de integração para rotas principais
"""
import pytest
from fastapi import status


@pytest.mark.integration
class TestMainRoutes:
    """Testes para rotas principais da API"""

    def test_root_endpoint(self, client):
        """Testa endpoint raiz"""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
