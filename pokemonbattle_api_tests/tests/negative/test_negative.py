import pytest

BASE_URL = "https://api.pokemonbattle.ru/v2"


@pytest.mark.negative
def test_get_trainer_invalid_id(session):
    response = session.get(
        f"{BASE_URL}/trainers",
        params={"trainer_id": -1}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Тренер отсутствует"