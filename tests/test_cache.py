from app.clients.pokeapi_client import PokeAPIClient


def test_get_pokemon_uses_cache_after_first_request(client, monkeypatch, pokemon_detail_payload):
    call_counter = {"count": 0}

    def fake_detail(identifier):
        call_counter["count"] += 1
        return pokemon_detail_payload

    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_detail", fake_detail)

    first_response = client.get("/pokemons/25")
    second_response = client.get("/pokemons/25")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert call_counter["count"] == 1
