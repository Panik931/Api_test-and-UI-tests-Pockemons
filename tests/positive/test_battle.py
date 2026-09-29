from pathlib import Path

import allure
import pytest
import yaml
from jsonschema import validate

from utils.constants import BASE_URL

BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_PATH = BASE_DIR / "schemas" / "battle_schema.yaml"


@allure.step("Загружаем JSON-схему битвы")
def load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as file:
        return yaml.safe_load(file)


@allure.title("GET /battle: проверка схемы ответа")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive
@pytest.mark.api
def test_get_battle_schema(session):
    with allure.step("Отправляем GET-запрос на получение данных о битвах"):
        response = session.get(f"{BASE_URL}/battle")

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step("Валидируем ответ по JSON-схеме"):
        data = response.json()
        validate(
            instance=data,
            schema=load_schema(),
        )