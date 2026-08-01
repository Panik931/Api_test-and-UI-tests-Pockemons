# --- ЗАДАНИЕ  2 ---
import requests

# Глобальные константы
TRAINERS_URL = "https://api.pokemonbattle.ru/v2/trainers"
BASE_URL = "https://api.pokemonbattle.ru/v2"
TOKEN = "8f36a308c11872d3941dd3c906f19b16"
TRAINER_ID = 66134


session = requests.Session()
session.headers.update({"trainer_token": TOKEN})

def test_get_trainers_by_city():
    city = "Москва"
    response = session.get(TRAINERS_URL, params={"city": city})
    assert response.status_code == 200

    data = response.json()["data"]
    for trainer in data:
        assert trainer["city"].lower() == city.lower()


def test_get_trainer_by_id():
    response = session.get(TRAINERS_URL, params={"trainer_id": TRAINER_ID})
    assert response.status_code == 200

    data = response.json()["data"]
    assert len(data) == 1
    assert int(data[0]["id"]) == TRAINER_ID


def test_get_trainers_by_city_sorted_desc():
    city = "Москва"
    response = session.get(TRAINERS_URL, params={"city": city})
    assert response.status_code == 200

    data = response.json()["data"]

    # 1. Проверяем город (независимо от регистра)
    for trainer in data:
        assert trainer["city"].lower() == city.lower()

    # 2. Сортируем список тренеров по убыванию уровня
    sorted_trainers = sorted(
        data,
        key=lambda x: int(x.get("level", 0)),
        reverse=True
    )

    # 3. Проверяем, что первый тренер имеет максимальный уровень в списке
    levels = [int(t["level"]) for t in sorted_trainers if "level" in t]
    assert levels[0] == max(levels), "Сортировка по убыванию сформирована неверно"


# --- ЗАДАНИЕ 3 ---

def knockout_all_pokemons():
    response = session.get(f"{BASE_URL}/pokemons", params={"trainer_id": TRAINER_ID})
    pokemons = response.json().get("data", [])

    for pokemon in pokemons:
        if str(pokemon.get("status")) == "1":
            session.post(
                f"{BASE_URL}/pokemons/knockout",
                json={"pokemon_id": pokemon["id"]}
            )

    # Проверяем, что все покемоны в нокауте
    response = session.get(f"{BASE_URL}/pokemons", params={"trainer_id": TRAINER_ID})
    pokemons = response.json().get("data", [])
    for pokemon in pokemons:
        assert int(pokemon["status"]) == 0


def create_pokemon():
    response = session.post(
        f"{BASE_URL}/pokemons",
        json={
            "name": "TestPokemon",
            "photo_id": 1
        }
    )
    assert response.status_code in (200, 201)
    return response.json()["id"] if "id" in response.json() else response.json()["data"]["id"]


def test_patch_pokemon_name():
    knockout_all_pokemons()

    pokemon_id = create_pokemon()

    new_name = "SuperPokemon"
    response = session.patch(
        f"{BASE_URL}/pokemons",
        json={
            "pokemon_id": pokemon_id,
            "name": new_name
        }
    )
    assert response.status_code == 200

    response = session.get(f"{BASE_URL}/pokemons", params={"trainer_id": TRAINER_ID})
    pokemons = response.json()["data"]

    pokemon = next(p for p in pokemons if int(p["id"]) == int(pokemon_id))
    assert pokemon["name"] == new_name