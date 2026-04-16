def test_get_pokemon_by_id_success(client, pokemon_payload):
    create_response = client.post("/pokemons", json=pokemon_payload)
    pokemon_id = create_response.json()["id"]

    response = client.get(f"/pokemons/{pokemon_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pokemon_id
    assert data["nome"] == "Pikachu"


def test_get_pokemon_by_id_not_found(client):
    response = client.get("/pokemons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado."
