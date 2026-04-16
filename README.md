# Pokemon API

Projeto final do curso **Back-End Python EBAC**, desenvolvido com **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Poetry**, **Pytest**, **GitHub Actions** e **Render**.

A proposta do projeto é entregar uma API inspirada na **PokeAPI**, consumindo dados diretamente da API oficial, transformando o retorno em um formato padronizado e disponibilizando endpoints documentados, testados, dockerizados e publicados em produção.

---

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Poetry
- Pytest
- Pytest-Cov
- Ruff
- Docker / Docker Compose
- GitHub Actions
- Render

---

## Funcionalidades

- Listar pokémons com paginação
- Buscar um pokémon por ID
- Consumir dados diretamente da PokeAPI
- Cache local com banco relacional usando SQLAlchemy
- Documentação automática com Swagger e ReDoc
- Testes automatizados com cobertura
- CI com GitHub Actions
- Deploy em produção no Render

---

## API em produção

- Base URL: `https://pokemon-api-ebac.onrender.com`
- Health check: `https://pokemon-api-ebac.onrender.com/health`
- Swagger: `https://pokemon-api-ebac.onrender.com/docs`
- ReDoc: `https://pokemon-api-ebac.onrender.com/redoc`

> Observação: por estar no plano gratuito do Render, a primeira requisição pode demorar alguns segundos caso a instância esteja inativa.

---

## Estrutura do projeto

```text
pokemon-api/
├── .github/
│   └── workflows/
│       └── ci.yml
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
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## Endpoints

### Health check
- `GET /health`

### Listar pokémons
- `GET /pokemons`
- Query params:
  - `limit`
  - `offset`

### Buscar pokémon por ID
- `GET /pokemons/{pokemon_id}`

---

## Formato das respostas

### `GET /pokemons?limit=5&offset=0`

```json
{
  "data": [
    {
      "name": "bulbasaur",
      "id": 1,
      "height": 7,
      "weight": 69,
      "types": [
        "grass",
        "poison"
      ],
      "sprites": {
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png"
      }
    }
  ],
  "pagination": {
    "total": 1350,
    "limit": 5,
    "offset": 0,
    "next": "/pokemons?limit=5&offset=5",
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
  "types": [
    "electric"
  ],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png"
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
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@localhost:5432/pokemon_db
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
CACHE_TTL_MINUTES=60
REQUEST_TIMEOUT_SECONDS=20
```

### Observação sobre o `DATABASE_URL`

Existem dois cenários:

#### 1. Rodando localmente com Poetry
Use `localhost`:

```env
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@localhost:5432/pokemon_db
```

#### 2. Rodando via Docker Compose
Use `db`, que é o nome do serviço no compose:

```env
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db
```

#### 3. Rodando em produção no Render
Use a connection string do banco Render no formato:

```env
DATABASE_URL=postgresql+psycopg://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO
```

---

## Como executar localmente com Poetry

### 1. Clonar o repositório

```bash
git clone https://github.com/igormoser/Projeto_Final-Back-End-EBAC.git
cd Projeto_Final-Back-End-EBAC
```

### 2. Criar o arquivo `.env`

#### Linux / macOS
```bash
cp .env.example .env
```

#### Windows
Copie o arquivo `.env.example` e renomeie para `.env`.

### 3. Ajustar o `DATABASE_URL`
- local com Poetry: `localhost`
- compose: `db`

### 4. Instalar dependências

```bash
poetry install
```

### 5. Subir o banco PostgreSQL

#### Docker
```bash
docker compose up -d db
```

#### Podman
```bash
podman machine start
podman compose up -d db
```

### 6. Rodar a API

```bash
poetry run uvicorn app.main:app --reload
```

### 7. Acessar a documentação

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

## Como executar com Podman Compose

```bash
podman machine start
podman compose up --build -d
```

A aplicação ficará disponível em:

- `http://localhost:8000/docs`

Para derrubar os containers:

```bash
podman compose down
```

---

## Como rodar os testes

### Testes
```bash
poetry run pytest
```

### Lint
```bash
poetry run ruff check .
```

### Cobertura
```bash
poetry run pytest --cov=app --cov-report=term-missing --cov-report=xml
```

---

## CI/CD

O projeto possui workflow de CI com **GitHub Actions**, executando:

- instalação de dependências
- lint com Ruff
- testes automatizados
- geração de cobertura

Além disso, o deploy está configurado no **Render**, com atualização a partir da branch principal.

---

## Observações finais

- Os dados são consumidos diretamente da **PokeAPI**
- O banco relacional é utilizado como suporte/cache local
- A API está publicada em produção no Render
- A documentação está disponível publicamente via Swagger
- O projeto foi estruturado com separação entre rotas, client externo, services, schemas, models, db e configuração

---

## Autor

**Igor Moser**  
Projeto acadêmico do curso **Back-End Python EBAC**
