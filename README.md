# Projeto Inspeção Sanitária

Projeto full-stack para gestão de inspeções sanitárias, desenvolvido com FastAPI (backend) e Next.js (frontend).


## Pensamentos e Modelagem de Dados para Concepção

![Imagem da Modelagem do Sistema](/images/modelagem.png)
![Representacao do Fluxo Padrão](/images/fluxo.png)
![Coverage Testes Backend](/images/coverage.png)


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
- **TypeScript** - Tipagem estática
- **React Query** - Gerenciamento de estado e cache de requisições
- **Axios** - Cliente HTTP

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

## 💡 Decisões Técnicas e de Negócio

### Modelagem de Dados e Auditoria

#### Sistema de Logs para Rastreabilidade
Foi implementado um sistema completo de logs para todas as entidades que possuem campos passíveis de alteração, especificamente **Inspeções** e **Irregularidades**. Esta decisão foi tomada para garantir:

- **Rastreabilidade completa**: Histórico de todas as alterações realizadas
- **Auditoria**: Possibilidade de identificar quem fez cada alteração e quando
- **Conformidade**: Atendimento a requisitos de rastreabilidade em inspeções sanitárias
- **Transparência**: Visibilidade total do processo de inspeção

As tabelas de log (`inspection_log` e `irregularities_log`) armazenam:
- O estado anterior e novo estado dos campos alterados
- O inspetor responsável pela alteração
- Timestamp da alteração

#### Inclusão do Usuário nos Logs
Uma decisão importante de modelagem foi incluir o campo `inspector_id` em todos os logs, mesmo quando a entidade principal já possui essa informação. Isso se justifica porque:

- **Múltiplos usuários na mesma inspeção**: Diferentes inspetores podem trabalhar na mesma inspeção em momentos diferentes
- **Rastreabilidade individual**: Cada alteração precisa ser atribuída ao inspetor específico que a realizou
- **Responsabilização**: Permite identificar claramente quem foi responsável por cada mudança no estado da inspeção ou irregularidade

### Desafios de Modelagem de Negócio

#### Complexidade dos Status
A modelagem dos status de inspeção e irregularidades apresentou desafios significativos devido ao **pouco conhecimento específico na área de inspeção sanitária**. As decisões foram tomadas com base em:

- Pesquisa sobre processos de inspeção sanitária
- Necessidade de cobrir diferentes cenários (inspeção livre, com irregularidades, interdição, etc.)
- Flexibilidade para ajustes futuros conforme o conhecimento do domínio evolui

Os status implementados incluem:
- **Inspeções**: Livre, Com Irregularidades, Interdição Imediata, Finalizada, Finalizada com Interdição, Finalizada com Interdição Parcial
- **Irregularidades**: Baixa, Moderada, Alta, Crítica, Resolvida

### Arquitetura e Organização

#### Estrutura de Arquivos
A organização do projeto seguiu as **melhores práticas recomendadas pelas documentações oficiais** tanto do FastAPI quanto do Next.js:

**Backend (FastAPI)**:
- Separação clara entre `models`, `schemas`, `routes` e `services`
- Uso de `core` para configurações centrais (database, security, config)
- Estrutura modular que facilita manutenção e escalabilidade

**Frontend (Next.js)**:
- Uso do App Router do Next.js 14
- Organização por features e componentes reutilizáveis
- Separação de concerns (hooks, contexts, lib)

#### Arquitetura de Serviços
A decisão de criar uma camada de **services** foi tomada pensando em:

- **Reutilização de lógica**: Evitar duplicação de código entre rotas
- **Comunicação entre serviços**: Permitir que serviços conversem entre si quando necessário
- **Exemplo prático**: O `IrregularityService` se comunica com o `InspectionService` para atualizar automaticamente o status da inspeção quando uma irregularidade é criada ou modificada
- **Testabilidade**: Facilita a criação de testes unitários isolados
- **Manutenibilidade**: Lógica de negócio centralizada e fácil de modificar

### Decisões de Frontend

#### Ausência de Biblioteca de Design
Optou-se por **não utilizar bibliotecas de design** (como Ant Design, Material-UI, Tailwind CSS, etc.) pelos seguintes motivos:

- **Simplicidade do projeto**: O escopo não justificava a complexidade adicional
- **Bundle size reduzido**: Aplicação mais leve e rápida
- **Controle total**: Maior flexibilidade para customização específica
- **CSS Modules**: Uso de CSS Modules nativo do Next.js para estilização

#### React Query para Gerenciamento de Estado
A escolha do **React Query** foi estratégica para:

- **Cache inteligente**: Evita requisições repetidas desnecessárias
- **Performance em dispositivos móveis**: Reduz consumo de dados e bateria
- **Experiência do usuário**: Interface mais fluida mesmo com conexão lenta
- **Otimização para celulares fracos**: Menor processamento no cliente
- **Sincronização automática**: Atualização de dados em background
- **Gerenciamento de loading e error states**: Simplifica o tratamento de estados assíncronos

#### Design Responsivo e Mobile-First
O CSS foi desenvolvido com **foco em compatibilidade com dispositivos móveis**:

- Layout responsivo que se adapta a diferentes tamanhos de tela
- Otimizações para touch (botões maiores, espaçamento adequado)
- Consideração de limitações de dispositivos móveis (processamento, memória, conexão)
- Interface simplificada para usuários com pouco contato com tecnologia

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
