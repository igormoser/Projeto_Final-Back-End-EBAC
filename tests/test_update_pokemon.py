def test_update_pokemon_success(client):
    create_payload = {
        "id": 9002,
        "name": "testmon",
        "height": 8,
        "weight": 120,
        "types": ["fire"],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }
    client.post("/pokemons", json=create_payload)

    update_payload = {
        "name": "testmon-evolved",
        "height": 12,
        "weight": 180,
        "types": ["fire", "flying"],
        "sprites": {
            "front_default": "https://example.com/front2.png",
            "back_default": "https://example.com/back2.png",
        },
    }

    response = client.put("/pokemons/9002", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testmon-evolved"
    assert data["types"] == ["fire", "flying"]