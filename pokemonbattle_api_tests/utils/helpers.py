BASE_URL = "https://api.pokemonbattle.ru/v2"
TRAINERS_URL = f"{BASE_URL}/trainers"
TRAINER_ID = 66134


def knockout_all_pokemons(session):
    response = session.get(
        f"{BASE_URL}/pokemons",
        params={
            "trainer_id": TRAINER_ID
        }
    )

    assert response.status_code == 200

    pokemons = response.json()["data"]

    for pokemon in pokemons:
        if int(pokemon["status"]) == 1:
            session.post(
                f"{BASE_URL}/pokemons/knockout",
                json={
                    "pokemon_id": pokemon["id"]
                }
            )

    response = session.get(
        f"{BASE_URL}/pokemons",
        params={
            "trainer_id": TRAINER_ID
        }
    )

    pokemons = response.json()["data"]

    for pokemon in pokemons:
        assert int(pokemon["status"]) == 0


def create_pokemon(session):
    response = session.post(
        f"{BASE_URL}/pokemons",
        json={
            "name": "TestPokemon",
            "photo_id": 1
        }
    )

    assert response.status_code == 201

    return response.json()["id"]