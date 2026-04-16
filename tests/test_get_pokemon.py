from app.clients.pokeapi_client import PokeAPIClient


def test_get_pokemon_by_id_success(client, monkeypatch, pokemon_detail_payload):
    def fake_detail(identifier):
        return pokemon_detail_payload

    monkeypatch.setattr(PokeAPIClient, "fetch_pokemon_detail", fake_detail)

    response = client.get("/pokemons/25")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 25
    assert data["name"] == "pikachu"
    assert data["types"] == ["electric"]
    assert data["sprites"]["front_default"] is not None
