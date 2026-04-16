import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["APP_NAME"] = "Pokemon API - Testes"
os.environ["APP_VERSION"] = "1.0.0-test"
os.environ["APP_DESCRIPTION"] = "Ambiente de testes"

from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def pokemon_payload() -> dict:
    return {
        "nome": "Pikachu",
        "numero_pokedex": 25,
        "tipo_primario": "Electric",
        "tipo_secundario": None,
        "altura": 0.4,
        "peso": 6.0,
        "descricao": "Pokémon elétrico muito ágil.",
    }
