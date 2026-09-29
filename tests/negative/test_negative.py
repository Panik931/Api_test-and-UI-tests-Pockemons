import allure
import pytest

from utils.helpers import BASE_URL


@allure.title("GET /trainers: запрос с невалидным trainer_id")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.negative
@pytest.mark.api
def test_get_trainer_invalid_id(session):
    with allure.step("Отправляем GET-запрос с невалидным trainer_id=-1"):
        response = session.get(
            f"{BASE_URL}/trainers",
            params={"trainer_id": -1},
        )

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    body = response.json()

    with allure.step("Проверяем, что в ответе статус 'error' и сообщение 'Тренер отсутствует'"):
        assert body["status"] == "error"
        assert body["message"] == "Тренер отсутствует"