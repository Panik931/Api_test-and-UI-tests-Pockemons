import time

import allure

from utils.constants import BASE_URL, TRAINERS_URL, TRAINER_ID


@allure.step("Переводим всех живых покемонов тренера в нокаут")
def knockout_all_pokemons(session):
    """Переводит всех живых покемонов тренера в нокаут."""

    with allure.step("Получаем список покемонов тренера"):
        response = session.get(
            f"{BASE_URL}/pokemons",
            params={"trainer_id": TRAINER_ID},
        )
        assert response.status_code == 200
        pokemons = response.json()["data"]

    for pokemon in pokemons:
        if int(pokemon["status"]) == 1:
            with allure.step(f"Отправляем в нокаут покемона с id={pokemon['id']}"):
                session.post(
                    f"{BASE_URL}/pokemons/knockout",
                    json={"pokemon_id": pokemon["id"]},
                )

    # Даём API время обновить статусы
    time.sleep(1)

    with allure.step("Проверяем, что все покемоны в нокауте"):
        # Делаем до 3 попыток проверки
        for attempt in range(3):
            response = session.get(
                f"{BASE_URL}/pokemons",
                params={"trainer_id": TRAINER_ID},
            )
            assert response.status_code == 200
            pokemons = response.json()["data"]

            all_knocked_out = all(int(pokemon["status"]) == 0 for pokemon in pokemons)

            if all_knocked_out:
                break

            if attempt < 2:
                with allure.step(f"Не все покемоны в нокауте, ожидание 1 сек (попытка {attempt + 1}/3)"):
                    time.sleep(1)
        else:
            # Если после 3 попыток не все в нокауте - падаем
            assert False, f"Не удалось перевести всех покемонов в нокаут. Текущие статусы: {[p['status'] for p in pokemons]}"


@allure.step("Создаём тестового покемона")
def create_pokemon(session):
    response = session.post(
        f"{BASE_URL}/pokemons",
        json={
            "name": "TestPokemon",
            "photo_id": 1,
        },
    )
    assert response.status_code == 201

    return response.json()["id"]