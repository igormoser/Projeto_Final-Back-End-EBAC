def test_delete_pokemon_success(client):
    payload = {
        "id": 9003,
        "name": "deletemon",
        "height": 9,
        "weight": 140,
        "types": ["ghost"],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }
    client.post("/pokemons", json=payload)

    response = client.delete("/pokemons/9003")

    assert response.status_code == 200
    assert response.json()["pokemon"]["id"] == 9003

    response_after = client.get("/pokemons/9003")
    assert response_after.status_code == 404