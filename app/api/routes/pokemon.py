from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pokemon import (
    PokemonCreate,
    PokemonDeleteResponse,
    PokemonListResponse,
    PokemonResponse,
    PokemonUpdate,
)
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

@router.post(
    "",
    response_model=PokemonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar pokémon local",
    description="Cria um pokémon local no banco de dados.",
)
def create_pokemon(payload: PokemonCreate, db: DBSession) -> PokemonResponse:
    return PokemonService.create_pokemon(db, payload)

@router.put(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Atualizar pokémon local",
    description="Atualiza um pokémon local salvo no banco.",
)
def update_pokemon(
    pokemon_id: int,
    payload: PokemonUpdate,
    db: DBSession,
) -> PokemonResponse:
    return PokemonService.update_pokemon(db, pokemon_id, payload)

@router.delete(
    "/{pokemon_id}",
    response_model=PokemonDeleteResponse,
    summary="Deletar pokémon local",
    description="Remove um pokémon local salvo no banco.",
)
def delete_pokemon(pokemon_id: int, db: DBSession) -> PokemonDeleteResponse:
    deleted = PokemonService.delete_pokemon(db, pokemon_id)
    return PokemonDeleteResponse(
        message="Pokémon local deletado com sucesso.",
        pokemon=deleted,
    )