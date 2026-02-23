# Frontend - Sistema de Inspeção Sanitária

Frontend desenvolvido em Next.js 14 para o sistema de gestão de inspeções sanitárias.

## Características

- **UI/UX simples e intuitiva** - Otimizado para uso em dispositivos móveis
- **Autenticação** - Sistema de login com token JWT
- **Gestão de Inspeções** - Criar, visualizar e finalizar inspeções
- **Gestão de Irregularidades** - Adicionar irregularidades às inspeções
- **Busca de Estabelecimentos** - Busca em tempo real por nome

## Tecnologias

- Next.js 14
- React 18
- TypeScript
- Axios
- CSS Modules

## Configuração

1. Instale as dependências:
```bash
npm install
```

2. Configure a URL da API no arquivo `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

## Estrutura

- `/app` - Páginas e rotas do Next.js
- `/components` - Componentes reutilizáveis
- `/contexts` - Contextos React (Auth)
- `/lib` - Utilitários, tipos e API client

## Funcionalidades

### Autenticação
- Login com usuário e senha
- Gerenciamento automático de token
- Redirecionamento automático se não autenticado

### Inspeções
- Lista de todas as inspeções
- Criar nova inspeção com busca de estabelecimento
- Visualizar detalhes da inspeção
- Finalizar inspeção com status e questões pendentes

### Irregularidades
- Adicionar irregularidades a uma inspeção
- Visualizar todas as irregularidades de uma inspeção
- Campos: descrição, severidade, interrupção imediata

## Notas

- O sistema é otimizado para uso em dispositivos móveis
- Interface simples e direta para usuários sem muito contato com tecnologia
- Todas as requisições incluem autenticação automática via token
