def test_update_pokemon_success(client, pokemon_payload):
    create_response = client.post("/pokemons", json=pokemon_payload)
    pokemon_id = create_response.json()["id"]

    updated_payload = {
        "nome": "Raichu",
        "numero_pokedex": 26,
        "tipo_primario": "Electric",
        "tipo_secundario": None,
        "altura": 0.8,
        "peso": 30.0,
        "descricao": "Forma evoluída do Pikachu.",
    }

    response = client.put(f"/pokemons/{pokemon_id}", json=updated_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Raichu"
    assert data["numero_pokedex"] == 26
    assert data["peso"] == 30.0


def test_update_pokemon_not_found(client, pokemon_payload):
    response = client.put("/pokemons/999", json=pokemon_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado."
