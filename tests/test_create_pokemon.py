def test_create_pokemon_success(client):
    payload = {
        "id": 9001,
        "name": "igorchu",
        "height": 10,
        "weight": 250,
        "types": ["electric"],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }

    response = client.post("/pokemons", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 9001
    assert data["name"] == "igorchu"
    assert data["types"] == ["electric"]