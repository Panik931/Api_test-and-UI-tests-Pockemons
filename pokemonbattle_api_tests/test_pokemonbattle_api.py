BASE_URL = "https://api.pokemonbattle.ru/v2"
TRAINERS_URL = f"{BASE_URL}/trainers"

TRAINER_ID = 66134


# -----------------------------
# Вспомогательные функции
# -----------------------------

def knockout_all_pokemons(session):
    """Переводит всех живых покемонов тренера в нокаут."""

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


# -----------------------------
# Тесты GET /trainers
# -----------------------------

def test_get_trainers_by_city(session):
    city = "Москва"

    response = session.get(
        TRAINERS_URL,
        params={
            "city": city
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    for trainer in data:
        assert trainer["city"].lower() == city.lower()


def test_get_trainer_by_id(session):

    response = session.get(
        TRAINERS_URL,
        params={
            "trainer_id": TRAINER_ID
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert len(data) == 1
    assert int(data[0]["id"]) == TRAINER_ID


def test_get_trainers_by_city_sorted_desc(session):

    city = "Москва"

    response = session.get(
        TRAINERS_URL,
        params={
            "city": city,
            "sort": "desc_level"
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    for trainer in data:
        assert trainer["city"].lower() == city.lower()

    levels = [int(trainer["level"]) for trainer in data]

    assert levels == sorted(levels, reverse=True)


# -----------------------------
# Тест PATCH /pokemons
# -----------------------------

def test_patch_pokemon_name(session):

    knockout_all_pokemons(session)

    pokemon_id = create_pokemon(session)

    new_name = "SuperPokemon"

    response = session.patch(
        f"{BASE_URL}/pokemons",
        json={
            "pokemon_id": pokemon_id,
            "name": new_name
        }
    )

    assert response.status_code == 200

    response = session.get(
        f"{BASE_URL}/pokemons",
        params={
            "pokemon_id": pokemon_id
        }
    )

    assert response.status_code == 200

    pokemon = response.json()["data"][0]

    assert pokemon["name"] == new_name