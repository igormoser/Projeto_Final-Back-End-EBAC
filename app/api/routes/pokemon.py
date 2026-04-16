from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pokemon import PokemonListResponse, PokemonResponse
from app.services.pokemon_service import PokemonService

router = APIRouter(prefix="/pokemons", tags=["Pokémons"])
DBSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=PokemonListResponse,
    summary="Listar pokémons",
    description="Lista pokémons paginados consumindo dados diretamente da PokeAPI.",
)
def list_pokemons(
    db: DBSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PokemonListResponse:
    return PokemonService.list_pokemons(db, limit=limit, offset=offset)


@router.get(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Buscar pokémon por ID",
    description="Retorna os detalhes de um pokémon específico consumindo dados da PokeAPI.",
)
def get_pokemon(pokemon_id: int, db: DBSession) -> PokemonResponse:
    return PokemonService.get_pokemon_by_id(db, pokemon_id)
