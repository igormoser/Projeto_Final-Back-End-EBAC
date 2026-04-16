from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.pokemon import Pokemon
from app.schemas.pokemon import PokemonCreate, PokemonUpdate


class PokemonService:
    @staticmethod
    def create_pokemon(db: Session, payload: PokemonCreate) -> Pokemon:
        existing = db.query(Pokemon).filter(
            or_(
                Pokemon.numero_pokedex == payload.numero_pokedex,
                Pokemon.nome == payload.nome,
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um pokémon com esse nome ou número da Pokédex.",
            )

        pokemon = Pokemon(**payload.model_dump())
        db.add(pokemon)
        db.commit()
        db.refresh(pokemon)
        return pokemon

    @staticmethod
    def list_pokemons(
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        nome: str | None = None,
        tipo: str | None = None,
    ) -> tuple[list[Pokemon], int]:
        query = db.query(Pokemon)

        if nome:
            query = query.filter(Pokemon.nome.ilike(f"%{nome.strip()}%"))

        if tipo:
            normalized_tipo = tipo.strip().title()
            query = query.filter(
                or_(
                    Pokemon.tipo_primario == normalized_tipo,
                    Pokemon.tipo_secundario == normalized_tipo,
                )
            )

        total = query.count()
        pokemons = query.order_by(Pokemon.id).offset(skip).limit(limit).all()
        return pokemons, total

    @staticmethod
    def get_pokemon_by_id(db: Session, pokemon_id: int) -> Pokemon:
        pokemon = db.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
        if pokemon is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokémon não encontrado.")
        return pokemon

    @staticmethod
    def update_pokemon(db: Session, pokemon_id: int, payload: PokemonUpdate) -> Pokemon:
        pokemon = PokemonService.get_pokemon_by_id(db, pokemon_id)

        duplicated = db.query(Pokemon).filter(
            Pokemon.id != pokemon_id,
            or_(
                Pokemon.numero_pokedex == payload.numero_pokedex,
                Pokemon.nome == payload.nome,
            )
        ).first()

        if duplicated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro pokémon com esse nome ou número da Pokédex.",
            )

        for field, value in payload.model_dump().items():
            setattr(pokemon, field, value)

        db.commit()
        db.refresh(pokemon)
        return pokemon

    @staticmethod
    def delete_pokemon(db: Session, pokemon_id: int) -> Pokemon:
        pokemon = PokemonService.get_pokemon_by_id(db, pokemon_id)
        db.delete(pokemon)
        db.commit()
        return pokemon
