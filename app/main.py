from fastapi import FastAPI

from app.api.routes.pokemon import router as pokemon_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.pokemon import Pokemon  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    contact={"name": "Igor Moser", "email": "igormoser@outlook.com"},
)

app.include_router(pokemon_router)


@app.get("/", tags=["Root"], summary="Mensagem inicial")
def read_root() -> dict[str, str]:
    return {"mensagem": "Bem-vindo à Pokemon API!"}


@app.get("/health", tags=["Health"], summary="Verificar saúde da API")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
