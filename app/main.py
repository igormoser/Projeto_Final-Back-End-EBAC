from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes.pokemon import router as pokemon_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine
from app.exceptions import PokemonNotFoundError, UpstreamServiceError
from app.models.pokemon_cache import PokemonCache  # noqa: F401  # noqa: F401
from app.models.pokemon_custom import PokemonCustom  # noqa: F401

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    contact={"name": "Igor Moser", "email": "igormoser@outlook.com"},
)

app.include_router(pokemon_router)


@app.exception_handler(PokemonNotFoundError)
def handle_pokemon_not_found(_, exc: PokemonNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UpstreamServiceError)
def handle_upstream_service_error(_, exc: UpstreamServiceError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/", tags=["Root"], summary="Mensagem inicial")
def read_root() -> dict[str, str]:
    return {"mensagem": "Bem-vindo à Pokemon API!"}


@app.get("/health", tags=["Health"], summary="Verificar saúde da API")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
