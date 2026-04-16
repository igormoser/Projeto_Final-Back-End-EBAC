import json
import logging
from datetime import UTC, datetime, timedelta
from urllib.parse import parse_qs, urlparse

from sqlalchemy.orm import Session

from app.clients.pokeapi_client import PokeAPIClient
from app.core.config import settings
from app.models.pokemon_cache import PokemonCache
from app.schemas.pokemon import (
    PaginationResponse,
    PokemonListResponse,
    PokemonResponse,
    PokemonSprites,
)

logger = logging.getLogger(__name__)


class PokemonService:
    @staticmethod
    def list_pokemons(db: Session, *, limit: int, offset: int) -> PokemonListResponse:
        logger.info("event=list_pokemons limit=%s offset=%s", limit, offset)
        listing = PokeAPIClient.fetch_pokemon_list(limit=limit, offset=offset)
        data = [
            PokemonService._get_pokemon_response(db, item.get("url") or item["name"])
            for item in listing["results"]
        ]

        return PokemonListResponse(
            data=data,
            pagination=PaginationResponse(
                total=listing["count"],
                limit=limit,
                offset=offset,
                next=PokemonService._to_relative_page_url(listing.get("next")),
                previous=PokemonService._to_relative_page_url(listing.get("previous")),
            ),
        )

    @staticmethod
    def get_pokemon_by_id(db: Session, pokemon_id: int) -> PokemonResponse:
        logger.info("event=get_pokemon_by_id pokemon_id=%s", pokemon_id)
        return PokemonService._get_pokemon_response(db, pokemon_id)

    @staticmethod
    def _get_pokemon_response(db: Session, identifier: int | str) -> PokemonResponse:
        pokemon_id = PokemonService._extract_pokemon_id(identifier)
        cached = PokemonService._get_valid_cache(db, pokemon_id)
        if cached is not None:
            logger.info("event=cache_hit pokemon_id=%s", pokemon_id)
            raw_payload = json.loads(cached.payload_json)
            return PokemonService._transform_pokemon_payload(raw_payload)

        logger.info("event=cache_miss pokemon_id=%s", pokemon_id)
        raw_payload = PokeAPIClient.fetch_pokemon_detail(identifier)
        PokemonService._upsert_cache(db, raw_payload)
        return PokemonService._transform_pokemon_payload(raw_payload)

    @staticmethod
    def _transform_pokemon_payload(payload: dict) -> PokemonResponse:
        return PokemonResponse(
            name=payload["name"],
            id=payload["id"],
            height=payload["height"],
            weight=payload["weight"],
            types=[item["type"]["name"] for item in payload.get("types", [])],
            sprites=PokemonSprites(
                front_default=payload.get("sprites", {}).get("front_default"),
                back_default=payload.get("sprites", {}).get("back_default"),
            ),
        )

    @staticmethod
    def _upsert_cache(db: Session, payload: dict) -> None:
        pokemon_id = payload["id"]
        cache = db.query(PokemonCache).filter(PokemonCache.pokemon_id == pokemon_id).first()
        serialized_payload = json.dumps(payload, ensure_ascii=False)

        if cache is None:
            cache = PokemonCache(
                pokemon_id=pokemon_id,
                name=payload["name"],
                payload_json=serialized_payload,
            )
            db.add(cache)
        else:
            cache.name = payload["name"]
            cache.payload_json = serialized_payload
            cache.fetched_at = datetime.now(UTC)

        db.commit()

    @staticmethod
    def _get_valid_cache(db: Session, pokemon_id: int | None) -> PokemonCache | None:
        if pokemon_id is None:
            return None

        cache = db.query(PokemonCache).filter(PokemonCache.pokemon_id == pokemon_id).first()
        if cache is None:
            return None

        fetched_at = cache.fetched_at
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=UTC)

        expiration = fetched_at + timedelta(minutes=settings.cache_ttl_minutes)
        if expiration < datetime.now(UTC):
            return None
        return cache

    @staticmethod
    def _to_relative_page_url(url: str | None) -> str | None:
        if not url:
            return None

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        limit = params.get("limit", [None])[0]
        offset = params.get("offset", [None])[0]

        if limit is None or offset is None:
            return None

        return f"/pokemons?limit={limit}&offset={offset}"

    @staticmethod
    def _extract_pokemon_id(identifier: int | str) -> int | None:
        if isinstance(identifier, int):
            return identifier

        if isinstance(identifier, str) and identifier.startswith("http"):
            try:
                return int(identifier.rstrip("/").split("/")[-1])
            except (TypeError, ValueError):
                return None

        try:
            return int(identifier)
        except (TypeError, ValueError):
            return None
