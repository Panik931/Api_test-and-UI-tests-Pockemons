import json

import allure
import pytest
import pytest_check as check

BASE_URL = "https://api.pokemonbattle.ru/v2"
ACHIEVEMENTS_URL = f"{BASE_URL}/achievements"


@allure.title("GET /achievements: невалидное значение параметра is_reached")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.negative
def test_get_achievements_invalid_is_reached(session):
    params = {"is_reached": "invalid"}

    with allure.step("Отправляем GET-запрос с невалидным параметром is_reached"):
        allure.attach(
            json.dumps(params, indent=2, ensure_ascii=False),
            name="Параметры запроса",
            attachment_type=allure.attachment_type.JSON,
        )
        response = session.get(ACHIEVEMENTS_URL, params=params)

    with allure.step("Проверяем, что сервер вернул статус-код 422"):
        assert response.status_code == 422

    with allure.step("Проверяем, что в ответе статус 'error' "
                     "и сообщение содержит информацию об ошибке парсинга"):
        data = response.json()
        message_str = str(data["message"])

        check.equal(data["status"], "error")
        check.is_in("bool_parsing", message_str)
        check.is_in("is_reached", message_str)
        check.is_in("Input should be a valid boolean", message_str)