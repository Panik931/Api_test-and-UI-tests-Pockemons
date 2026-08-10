import pytest

from utils.helpers import TRAINERS_URL, TRAINER_ID

@pytest.mark.positive

def test_get_trainers_by_city(session):

    city = "Москва"

    response = session.get(
        TRAINERS_URL,
        params={
            "city": city
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    for trainer in data:
        assert trainer["city"].lower() == city.lower()


@pytest.mark.skip(reason="Пример пропуска теста")

def test_get_trainer_by_id(session):

    response = session.get(
        TRAINERS_URL,
        params={
            "trainer_id": TRAINER_ID
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert len(data) == 1
    assert int(data[0]["id"]) == TRAINER_ID

@pytest.mark.positive
def test_get_trainers_by_city_sorted_desc(session):

    city = "Москва"

    response = session.get(
        TRAINERS_URL,
        params={
            "city": city,
            "sort": "desc_level"
        }
    )

    assert response.status_code == 200

    data = response.json()["data"]

    for trainer in data:
        assert trainer["city"].lower() == city.lower()

    levels = [int(trainer["level"]) for trainer in data]

    assert levels == sorted(levels, reverse=True)

