import json

import allure
import pytest

from utils.constants import BASE_URL, TRAINER_ID
from utils.helpers import (
    create_pokemon,
    knockout_all_pokemons,
)


def get_pokemon(session, pokemon_id):
    """Возвращает покемона по его id."""
    response = session.get(
        f"{BASE_URL}/pokemons",
        params={"pokemon_id": pokemon_id},
    )
    assert response.status_code == 200, response.text
    return response.json()["data"][0]


@allure.title("E2E: битва покемона и проверка состояния после битвы")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive
def test_pokemon_battle_e2e(session):
    with allure.step("Подготовка: нокаутируем всех покемонов тренера"):
        knockout_all_pokemons(session)

    with allure.step("Создаём нового покемона для битвы"):
        pokemon_id = create_pokemon(session)

    with allure.step("Сажаем покемона в покебол через /trainers/add_pokeball"):
        response = session.post(
            f"{BASE_URL}/trainers/add_pokeball",
            json={"pokemon_id": str(pokemon_id)},
        )
        assert response.status_code == 200, response.text

    with allure.step("Проверяем, что покемон жив и в покеболе до битвы"):
        pokemon_before = get_pokemon(session, pokemon_id)
        assert int(pokemon_before["status"]) == 1
        assert int(pokemon_before["in_pokeball"]) == 1

    with allure.step("Ищем соперника: первый живой покемон другого тренера"):
        response = session.get(
            f"{BASE_URL}/trainers",
            params={"city": "Москва"},
        )
        assert response.status_code == 200, response.text
        trainers = response.json()["data"]
        defender_trainer = next(
            t for t in trainers
            if int(t["id"]) != int(TRAINER_ID)
        )

        response = session.get(
            f"{BASE_URL}/pokemons",
            params={"trainer_id": defender_trainer["id"]},
        )
        assert response.status_code == 200, response.text
        alive = [
            p for p in response.json()["data"]
            if int(p["status"]) == 1
        ]
        assert alive, "У соперника нет живых покемонов"
        defender_id = alive[0]["id"]

    with allure.step("Начинаем битву"):
        response = session.post(
            f"{BASE_URL}/battle",
            json={
                "attacking_pokemon": str(pokemon_id),
                "defending_pokemon": str(defender_id),
            },
        )
        assert response.status_code == 200, response.text
        battle = response.json()

        allure.attach(
            json.dumps(battle, indent=2, ensure_ascii=False),
            name="Ответ POST /battle",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Определяем исход битвы по полю result"):
        result = str(battle["result"])
        won = "победил" in result

    with allure.step("Получаем состояние покемона после битвы"):
        pokemon_after = get_pokemon(session, pokemon_id)

    if won:
        with allure.step("Покемон ПОБЕДИЛ: проверяем, что остался жив"):
            assert int(pokemon_after["status"]) == 1
    else:
        with allure.step("Покемон ПРОИГРАЛ: проверяем нокаут и отсутствие в покеболе"):
            assert int(pokemon_after["status"]) == 0
            assert int(pokemon_after["in_pokeball"]) == 0