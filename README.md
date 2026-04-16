# Pokemon API

Projeto final do curso **Back-End Python EBAC**, desenvolvido com **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Poetry**, **Pytest** e integração com a **PokeAPI**.

A proposta do projeto é expor uma API própria que **consome dados diretamente da PokeAPI**, adapta o formato de resposta, aplica paginação, mantém cache local em banco relacional e disponibiliza documentação automática, testes, cobertura e pipeline de CI.

---

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Poetry
- Pytest
- Pytest-Cov
- HTTPX
- Docker / Docker Compose
- Podman / Podman Compose
- GitHub Actions

---

## Funcionalidades

- Listar pokémons consumindo dados da PokeAPI
- Buscar pokémon por ID consumindo dados da PokeAPI
- Paginação com `limit` e `offset`
- Resposta padronizada com `data` e `pagination`
- Cache local com PostgreSQL e SQLAlchemy
- Documentação automática com Swagger e ReDoc
- Testes automatizados com cobertura
- Pipeline de CI com GitHub Actions

---

## Estrutura do projeto

```text
pokemon-api/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── pokemon.py
│   ├── clients/
│   │   └── pokeapi_client.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── pokemon_cache.py
│   ├── schemas/
│   │   └── pokemon.py
│   ├── services/
│   │   └── pokemon_service.py
│   ├── exceptions.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_cache.py
│   ├── test_errors.py
│   ├── test_get_pokemon.py
│   └── test_list_pokemons.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Endpoints

### Listar pokémons
- `GET /pokemons?limit=20&offset=0`

### Buscar pokémon por ID
- `GET /pokemons/{pokemon_id}`

### Health check
- `GET /health`

---

## Formato da resposta

### `GET /pokemons`

```json
{
  "data": [
    {
      "name": "pikachu",
      "id": 25,
      "height": 4,
      "weight": 60,
      "types": ["electric"],
      "sprites": {
        "front_default": "https://...",
        "back_default": "https://..."
      }
    }
  ],
  "pagination": {
    "total": 1281,
    "limit": 20,
    "offset": 0,
    "next": "/pokemons?limit=20&offset=20",
    "previous": null
  }
}
```

### `GET /pokemons/25`

```json
{
  "name": "pikachu",
  "id": 25,
  "height": 4,
  "weight": 60,
  "types": ["electric"],
  "sprites": {
    "front_default": "https://...",
    "back_default": "https://..."
  }
}
```

---

## Variáveis de ambiente

O projeto utiliza um arquivo `.env`.

### Exemplo de `.env`

```env
APP_NAME=Pokemon API
APP_VERSION=2.0.0
APP_DESCRIPTION=API integradora da PokeAPI para o projeto final EBAC.
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
CACHE_TTL_MINUTES=60
REQUEST_TIMEOUT_SECONDS=20
```

### Observação importante sobre o `DATABASE_URL`

Existem dois cenários:

#### 1. Rodando a API localmente com Poetry
Use `localhost` no host do banco:

```env
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@localhost:5432/pokemon_db
```

#### 2. Rodando tudo via Docker Compose / Podman Compose
Use `db`, que é o nome do serviço no compose:

```env
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db
```

---

## Como preparar o ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/igormoser/Projeto_Final-Back-End-EBAC.git
cd Projeto_Final-Back-End-EBAC
```

### 2. Criar o arquivo `.env`
Copie o arquivo de exemplo.

#### Linux / macOS
```bash
cp .env.example .env
```

#### Windows
Copie manualmente o arquivo `.env.example` e renomeie para `.env`.

### 3. Ajustar o `DATABASE_URL`
- Se for rodar **localmente com Poetry**, troque `db` por `localhost`
- Se for rodar **via Compose**, mantenha `db`

---

## Como executar localmente com Poetry

### 1. Instalar as dependências

```bash
poetry install
```

### 2. Subir apenas o banco PostgreSQL

#### Com Docker
```bash
docker compose up -d db
```

#### Com Podman
```bash
podman compose up -d db
```

### 3. Rodar a API

```bash
poetry run uvicorn app.main:app --reload
```

### 4. Acessar a documentação

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Como executar com Docker Compose

```bash
docker compose up --build -d
```

A aplicação ficará disponível em:

- `http://localhost:8000/docs`

Para derrubar os containers:

```bash
docker compose down
```

---

## Como rodar os testes

```bash
poetry run pytest
```

## Como gerar cobertura

```bash
poetry run pytest --cov=app --cov-report=term-missing --cov-report=xml
```

---

## Link de produção

Adicione aqui a URL pública após o deploy no Render.

Exemplo:

```text
https://seu-servico.onrender.com/docs
```

---

## Observações finais

- Os dados são extraídos diretamente da **PokeAPI**, conforme o requisito do projeto.  
- O banco **PostgreSQL** é usado como cache local para reduzir chamadas repetidas à API externa.  
- O projeto inclui pipeline de CI com GitHub Actions.  
- A documentação automática do FastAPI está disponível no Swagger e no ReDoc.  
- O endpoint `/health` pode ser usado como health check no deploy.  

---

## Autor

**Igor Moser**  
Projeto acadêmico do curso **Back-End Python EBAC**
