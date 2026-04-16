def test_create_pokemon_success(client, pokemon_payload):
    response = client.post("/pokemons", json=pokemon_payload)

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Pikachu"
    assert data["numero_pokedex"] == 25
    assert data["tipo_primario"] == "Electric"


def test_create_pokemon_duplicate_number_returns_409(client, pokemon_payload):
    client.post("/pokemons", json=pokemon_payload)

    duplicated = dict(pokemon_payload)
    duplicated["nome"] = "Raichu"

    response = client.post("/pokemons", json=duplicated)

    assert response.status_code == 409
    assert response.json()["detail"] == "Já existe um pokémon com esse nome ou número da Pokédex."
