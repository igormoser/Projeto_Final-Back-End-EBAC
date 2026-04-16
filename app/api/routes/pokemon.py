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


@router.post(
    "",
    response_model=PokemonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo pokémon",
    description="Cria um novo registro de pokémon na base de dados.",
)
def create_pokemon(payload: PokemonCreate, db: Session = Depends(get_db)) -> PokemonResponse:
    return PokemonService.create_pokemon(db, payload)


@router.get(
    "",
    response_model=PokemonListResponse,
    summary="Listar pokémons",
    description="Lista pokémons com paginação e filtros opcionais por nome e tipo.",
)
def list_pokemons(
    db: Session = Depends(get_db),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    nome: str | None = None,
    tipo: str | None = None,
) -> PokemonListResponse:
    pokemons, total = PokemonService.list_pokemons(
        db,
        skip=skip,
        limit=limit,
        nome=nome,
        tipo=tipo,
    )
    return PokemonListResponse(items=pokemons, total=total, skip=skip, limit=limit)


@router.get(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Buscar pokémon por ID",
    description="Retorna um único pokémon com base no ID informado.",
)
def get_pokemon(pokemon_id: int, db: Session = Depends(get_db)) -> PokemonResponse:
    return PokemonService.get_pokemon_by_id(db, pokemon_id)


@router.put(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Atualizar um pokémon",
    description="Atualiza todos os dados de um pokémon existente.",
)
def update_pokemon(
    pokemon_id: int,
    payload: PokemonUpdate,
    db: Session = Depends(get_db),
) -> PokemonResponse:
    return PokemonService.update_pokemon(db, pokemon_id, payload)


@router.delete(
    "/{pokemon_id}",
    response_model=PokemonDeleteResponse,
    summary="Deletar um pokémon",
    description="Remove um pokémon da base de dados pelo ID informado.",
)
def delete_pokemon(pokemon_id: int, db: Session = Depends(get_db)) -> PokemonDeleteResponse:
    deleted = PokemonService.delete_pokemon(db, pokemon_id)
    return PokemonDeleteResponse(mensagem="Pokémon deletado com sucesso.", pokemon=deleted)
