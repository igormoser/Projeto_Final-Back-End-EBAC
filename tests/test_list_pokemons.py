def test_list_pokemons_with_pagination(client, pokemon_payload):
    bulbasaur = {
        "nome": "Bulbasaur",
        "numero_pokedex": 1,
        "tipo_primario": "Grass",
        "tipo_secundario": "Poison",
        "altura": 0.7,
        "peso": 6.9,
        "descricao": "Pokémon semente.",
    }

    client.post("/pokemons", json=bulbasaur)
    client.post("/pokemons", json=pokemon_payload)

    response = client.get("/pokemons?skip=0&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["skip"] == 0
    assert data["limit"] == 1
    assert len(data["items"]) == 1


def test_list_pokemons_filter_by_type(client, pokemon_payload):
    client.post("/pokemons", json=pokemon_payload)

    squirtle = {
        "nome": "Squirtle",
        "numero_pokedex": 7,
        "tipo_primario": "Water",
        "tipo_secundario": None,
        "altura": 0.5,
        "peso": 9.0,
        "descricao": "Pokémon tartaruga.",
    }
    client.post("/pokemons", json=squirtle)

    response = client.get("/pokemons?tipo=Electric")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["nome"] == "Pikachu"
