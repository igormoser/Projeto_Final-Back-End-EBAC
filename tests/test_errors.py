from app.clients.pokeapi_client import PokeAPIClient
from app.exceptions import PokemonNotFoundError, UpstreamServiceError


def test_get_pokemon_not_found_returns_404(client, monkeypatch):
    def fake_detail(identifier):
        raise PokemonNotFoundError("Pokémon não encontrado.")

    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_detail", fake_detail)

    response = client.get("/pokemons/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado."


def test_list_pokemons_upstream_failure_returns_502(client, monkeypatch):
    def fake_list(limit: int, offset: int):
        raise UpstreamServiceError("PokeAPI indisponível no momento.")

    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_list", fake_list)

    response = client.get("/pokemons")

    assert response.status_code == 502
    assert response.json()["detail"] == "PokeAPI indisponível no momento."
