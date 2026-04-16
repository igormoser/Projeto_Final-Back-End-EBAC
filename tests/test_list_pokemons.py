from app.clients.pokeapi_client import PokeAPIClient


def test_list_pokemons_with_pagination(client, monkeypatch, pokemon_detail_payload):
    def fake_list(limit: int, offset: int) -> dict:
        assert limit == 20
        assert offset == 0
        return {
            "count": 1281,
            "next": "https://pokeapi.co/api/v2/pokemon?limit=20&offset=20",
            "previous": None,
            "results": [
                {"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
            ],
        }

    def fake_detail(identifier):
        return pokemon_detail_payload

    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_list", fake_list)
    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_detail", fake_detail)

    response = client.get("/pokemons?limit=20&offset=0")

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "pikachu"
    assert data["pagination"]["total"] == 1281
    assert data["pagination"]["limit"] == 20
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["next"] == "/pokemons?limit=20&offset=20"
    assert data["pagination"]["previous"] is None
