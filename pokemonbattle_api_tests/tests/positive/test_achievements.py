import re

import yaml
from deepdiff import DeepDiff
from jsonschema import validate

from utils.constants import BASE_URL


def load_schema():
    with open(
        "pokemonbattle_api_tests/schemas/achievements_schema.yaml",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def test_get_achievements_schema_and_body(session):

    response = session.get(
        f"{BASE_URL}/achievements"
    )

    assert response.status_code == 200

    actual = response.json()

    # Проверяем JSON Schema
    validate(
        instance=actual,
        schema=load_schema()
    )

    # Ожидаем список достижений.
    # is_reached исключаем, потому что API возвращает его не всегда.
    expected = {
        "data": [
            {"slug": "beginning"},
            {"slug": "out_of_battles"},
            {"slug": "self_knockout"},
            {"slug": "max_level"},
            {"slug": "one_vs_seven"},
            {"slug": "five_battles"},
            {"slug": "three_defends"}
        ]
    }

    diff = DeepDiff(
        expected,
        actual,
        exclude_regex_paths=[
            r"root\['data'\]\[\d+\]\['is_reached'\]"
        ]
    )

    assert diff == {}