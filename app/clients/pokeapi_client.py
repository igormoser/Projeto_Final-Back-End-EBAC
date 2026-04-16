import httpx

from app.core.config import settings
from app.exceptions import PokemonNotFoundError, UpstreamServiceError


class PokeAPIClient:
    @staticmethod
    def fetch_pokemon_list(limit: int, offset: int) -> dict:
        url = f"{settings.pokeapi_base_url.rstrip('/')}/pokemon"
        try:
            response = httpx.get(
                url,
                params={"limit": limit, "offset": offset},
                timeout=settings.request_timeout_seconds,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise UpstreamServiceError("Falha ao consultar a listagem da PokeAPI.") from exc
        except httpx.HTTPError as exc:
            raise UpstreamServiceError("PokeAPI indisponível no momento.") from exc

    @staticmethod
    def fetch_pokemon_detail(identifier: int | str) -> dict:
        if isinstance(identifier, str) and identifier.startswith("http"):
            url = identifier
        else:
            url = f"{settings.pokeapi_base_url.rstrip('/')}/pokemon/{identifier}"

        try:
            response = httpx.get(url, timeout=settings.request_timeout_seconds)
            if response.status_code == 404:
                raise PokemonNotFoundError("Pokémon não encontrado.")
            response.raise_for_status()
            return response.json()
        except PokemonNotFoundError:
            raise
        except httpx.HTTPStatusError as exc:
            raise UpstreamServiceError("Falha ao consultar o detalhe na PokeAPI.") from exc
        except httpx.HTTPError as exc:
            raise UpstreamServiceError("PokeAPI indisponível no momento.") from exc
