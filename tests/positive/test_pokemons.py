import json

import allure
import pytest

from utils.constants import BASE_URL
from utils.helpers import (
    knockout_all_pokemons,
    create_pokemon,
)


@allure.title("PATCH /pokemons: изменение имени покемона")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive
def test_patch_pokemon_name(session):
    with allure.step("Подготавливаем тестовые данные: отправляем всех покемонов в нокаут и создаём нового"):
        knockout_all_pokemons(session)
        pokemon_id = create_pokemon(session)

        allure.attach(
            str(pokemon_id),
            name="ID созданного покемона",
            attachment_type=allure.attachment_type.TEXT,
        )

    new_name = "SuperPokemon"

    allure.attach(
        new_name,
        name="Новое имя покемона",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("Изменяем имя покемона через PATCH-запрос"):
        response = session.patch(
            f"{BASE_URL}/pokemons",
            json={
                "pokemon_id": pokemon_id,
                "name": new_name,
            },
        )

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step("Получаем обновлённые данные покемона через GET-запрос"):
        response = session.get(
            f"{BASE_URL}/pokemons",
            params={"pokemon_id": pokemon_id},
        )
        pokemon = response.json()["data"][0]

    with allure.step("Проверяем, что имя покемона изменилось на новое"):
        assert pokemon["name"] == new_name