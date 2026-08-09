from pathlib import Path

import yaml
from jsonschema import validate


BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_PATH = BASE_DIR / "schemas" / "battle_schema.yaml"


def load_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as file:
        return yaml.safe_load(file)


def test_get_battle_schema(session):

    response = session.get(
        "https://api.pokemonbattle.ru/v2/battle"
    )

    assert response.status_code == 200

    data = response.json()

    validate(
        instance=data,
        schema=load_schema()
    )