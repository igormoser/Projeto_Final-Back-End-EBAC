def test_crud_flow_local_pokemon(client):
    create_payload = {
        "id": 9999,
        "name": "crudmon",
        "height": 11,
        "weight": 300,
        "types": ["dragon"],
        "sprites": {
            "front_default": "https://example.com/front.png",
            "back_default": "https://example.com/back.png",
        },
    }

    create_response = client.post("/pokemons", json=create_payload)
    assert create_response.status_code == 201

    get_response = client.get("/pokemons/9999")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "crudmon"

    update_payload = {
        "name": "crudmon-x",
        "height": 12,
        "weight": 320,
        "types": ["dragon", "dark"],
        "sprites": {
            "front_default": "https://example.com/front2.png",
            "back_default": "https://example.com/back2.png",
        },
    }

    update_response = client.put("/pokemons/9999", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "crudmon-x"

    delete_response = client.delete("/pokemons/9999")
    assert delete_response.status_code == 200

    final_get = client.get("/pokemons/9999")
    assert final_get.status_code == 404