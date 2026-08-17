import json
from pathlib import Path

import allure
import pytest
import yaml
from deepdiff import DeepDiff
from jsonschema import validate

from utils.constants import BASE_URL


@allure.step("Загружаем JSON-схему достижений")
def load_schema():
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "schemas"
        / "achievements_schema.yaml"
    )
    with open(schema_path, encoding="utf-8") as file:
        return yaml.safe_load(file)


@allure.title("GET /achievements: проверка схемы и списка достижений")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive
def test_get_achievements_schema_and_body(session):
    with allure.step("Отправляем GET-запрос на получение списка достижений"):
        response = session.get(f"{BASE_URL}/achievements")

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    actual = response.json()

    with allure.step("Валидируем ответ по JSON-схеме"):
        validate(
            instance=actual,
            schema=load_schema(),
        )

    # Ожидаем список достижений.
    expected = {
        "data": [
            {"slug": "beginning"},
            {"slug": "out_of_battles"},
            {"slug": "self_knockout"},
            {"slug": "max_level"},
            {"slug": "one_vs_seven"},
            {"slug": "five_battles"},
            {"slug": "three_defends"},
        ]
    }

    allure.attach(
        json.dumps(expected, indent=2, ensure_ascii=False),
        name="Ожидаемые данные",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Сравниваем список достижений с ожидаемым (без is_reached)"):
        diff = DeepDiff(
            expected,
            actual,
            exclude_regex_paths=[
                r"root\['data'\]\[\d+\]\['is_reached'\]"
            ],
        )
        assert diff == {}