# Testes do Backend

Este diretório contém os testes unitários e de integração para o backend da aplicação.

## Estrutura

```
tests/
├── __init__.py
├── conftest.py          # Fixtures globais
├── unit/                # Testes unitários
│   ├── __init__.py
│   ├── test_auth_service.py
│   ├── test_user_service.py
│   └── test_security.py
└── integration/         # Testes de integração
    ├── __init__.py
    ├── test_auth_routes.py
    ├── test_user_routes.py
    └── test_main.py
```

## Instalação

Instale as dependências de teste:

```bash
pip install -r requirements.txt
```

## Executando os Testes

### Executar todos os testes

```bash
pytest
```

### Executar apenas testes unitários

```bash
pytest tests/unit/ -m unit
```

### Executar apenas testes de integração

```bash
pytest tests/integration/ -m integration
```

### Executar um arquivo específico

```bash
pytest tests/unit/test_auth_service.py
```

### Executar com cobertura de código

```bash
pytest --cov=app --cov-report=html
```

Isso gerará um relatório em `htmlcov/index.html`.

### Executar em modo verbose

```bash
pytest -v
```

## Fixtures Disponíveis

As seguintes fixtures estão disponíveis em `conftest.py`:

- `db_session`: Sessão de banco de dados de teste (SQLite em memória)
- `client`: Cliente HTTP de teste (TestClient do FastAPI)
- `sample_user_data`: Dados de exemplo para criação de usuário
- `sample_user`: Usuário de exemplo criado no banco de dados
- `auth_headers`: Headers de autenticação para requisições autenticadas

## Escrevendo Novos Testes

### Teste Unitário

```python
import pytest
from app.services.auth import AuthService

@pytest.mark.unit
class TestMeuServico:
    def test_meu_metodo(self, db_session):
        service = AuthService(db_session)
        # Seu teste aqui
        assert True
```

### Teste de Integração

```python
import pytest
from fastapi import status

@pytest.mark.integration
class TestMinhaRota:
    def test_minha_rota(self, client, auth_headers):
        response = client.get("/api/minha-rota", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
```

## Marcadores

Os seguintes marcadores estão disponíveis:

- `@pytest.mark.unit`: Para testes unitários
- `@pytest.mark.integration`: Para testes de integração
- `@pytest.mark.slow`: Para testes que demoram mais tempo

Execute testes por marcador:

```bash
pytest -m unit
pytest -m integration
pytest -m "not slow"  # Exclui testes lentos
```

## Configuração

A configuração do pytest está em `pytest.ini` na raiz do backend.
