# Pokemon API

Projeto final do curso **Back-End Python EBAC**, desenvolvido com **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Poetry** e **Pytest**.

A proposta do projeto é entregar uma API inspirada na **PokéAPI**, com operações completas de **CRUD** para registros de pokémons, documentação automática com FastAPI, testes automatizados e execução local ou via containers.

---

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Poetry
- Pytest
- Docker / Docker Compose
- Podman / Podman Compose

---

## Funcionalidades

- Criar pokémons
- Listar pokémons com paginação
- Filtrar por nome e tipo
- Buscar um pokémon por ID
- Atualizar um pokémon
- Deletar um pokémon
- Documentação automática com Swagger e ReDoc
- Testes automatizados com Pytest
- Execução local e via containers

---

## Estrutura do projeto

```text
pokemon-api/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── pokemon.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── pokemon.py
│   ├── schemas/
│   │   └── pokemon.py
│   ├── services/
│   │   └── pokemon_service.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_create_pokemon.py
│   ├── test_list_pokemons.py
│   ├── test_get_pokemon.py
│   ├── test_update_pokemon.py
│   └── test_delete_pokemon.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Modelo do Pokémon

Cada registro possui os seguintes campos:

- `id`
- `nome`
- `numero_pokedex`
- `tipo_primario`
- `tipo_secundario`
- `altura`
- `peso`
- `descricao`
- `criado_em`
- `atualizado_em`

---

## Endpoints

### Criar um pokémon
- `POST /pokemons`

### Listar pokémons
- `GET /pokemons`
- Query params opcionais:
  - `skip`
  - `limit`
  - `nome`
  - `tipo`

### Buscar pokémon por ID
- `GET /pokemons/{pokemon_id}`

### Atualizar pokémon
- `PUT /pokemons/{pokemon_id}`

### Deletar pokémon
- `DELETE /pokemons/{pokemon_id}`

### Health check
- `GET /health`

---

## Variáveis de ambiente

O projeto utiliza um arquivo `.env`.

### Exemplo de `.env`

```env
APP_NAME=Pokemon API
APP_VERSION=1.0.0
APP_DESCRIPTION=API final do curso EBAC inspirada na PokéAPI.
DATABASE_URL=postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db
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
git clone <https://github.com/igormoser/Projeto_Final-Back-End-EBAC.git>
cd pokemon-api
```

### 2. Criar o arquivo `.env`
Copie o arquivo de exemplo:

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

## Como executar com Podman Compose

### 1. Iniciar a machine do Podman
Depois de ligar o computador, normalmente é necessário iniciar a machine:

```bash
podman machine start
```

### 2. Subir os containers

```bash
podman compose up --build -d
```

Se o seu ambiente não reconhecer `podman compose`, use:

```bash
podman-compose up --build -d
```

A aplicação ficará disponível em:

- `http://localhost:8000/docs`

Para derrubar os containers:

```bash
podman compose down
```

ou:

```bash
podman-compose down
```

---

## Como rodar os testes

```bash
poetry run pytest
```

---

## Exemplo de payload para criação

```json
{
  "nome": "Pikachu",
  "numero_pokedex": 25,
  "tipo_primario": "Electric",
  "tipo_secundario": null,
  "altura": 0.4,
  "peso": 6.0,
  "descricao": "Pokémon elétrico muito ágil."
}
```

---

## Validações do projeto

O projeto foi validado com:

- testes automatizados com `pytest`
- execução da API com `uvicorn`
- documentação interativa no Swagger
- testes manuais de CRUD no `/docs`

---

## Observações finais

- O banco principal do projeto é **PostgreSQL**
- Os testes utilizam **SQLite** isolado
- As tabelas são criadas automaticamente na inicialização da aplicação
- A listagem de pokémons possui paginação e filtros básicos
- O projeto foi estruturado para manter separação entre rotas, schemas, models, services e configuração

---

## Autor

**Igor Moser**  
Projeto acadêmico do curso **Back-End Python EBAC**
