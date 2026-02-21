# Projeto Inspeção Sanitária

Projeto full-stack para gestão de inspeções sanitárias, desenvolvido com FastAPI (backend) e Next.js (frontend).


## Pensamentos e Modelagem de Dados para Concepção

![Imagem da Modelagem do Sistema](/images/modelagem.png)
![Representacao do Fluxo Padrão](/images/fluxo.png)


## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido para Python
- **PostgreSQL** - Banco de dados relacional
- **JWT** - Autenticação baseada em tokens
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **Swagger/OpenAPI** - Documentação automática da API

### Frontend
- **Next.js** - Framework React para produção
- **TypeScript** - Tipagem estática (opcional)

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

## 📁 Estrutura do Projeto

```
inspecao-sanitária/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── users.py
│   │   └── db/
│   │       └── base.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🛠️ Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose instalados

### Passos

1. **Clone o repositório** (se aplicável)

2. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações.

3. **Inicie os containers:**
   ```bash
   docker-compose up -d
   ```

4. **Acesse os serviços:**
   - **Backend API**: http://localhost:8000
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **Frontend**: http://localhost:3000

### Comandos Úteis

```bash
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild containers
docker-compose up -d --build

# Executar comandos no backend
docker-compose exec backend bash

# Executar comandos no frontend
docker-compose exec frontend sh
```

## 🔐 Autenticação

O projeto utiliza JWT (JSON Web Tokens) para autenticação. Para obter um token:

1. Faça uma requisição POST para `/api/auth/login` com credenciais válidas
2. Use o token retornado no header `Authorization: Bearer <token>`

## 📚 Documentação da API

A documentação interativa está disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Desenvolvimento

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 Licença

Este projeto está sob licença MIT.
