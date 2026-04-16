def test_delete_pokemon_success(client, pokemon_payload):
    create_response = client.post("/pokemons", json=pokemon_payload)
    pokemon_id = create_response.json()["id"]

    response = client.delete(f"/pokemons/{pokemon_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["mensagem"] == "Pokémon deletado com sucesso."
    assert data["pokemon"]["id"] == pokemon_id


def test_delete_pokemon_not_found(client):
    response = client.delete("/pokemons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado."
