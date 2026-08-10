import pytest
import pytest_check as check

BASE_URL = "https://api.pokemonbattle.ru/v2"
ACHIEVEMENTS_URL = f"{BASE_URL}/achievements"


@pytest.mark.negative
def test_get_achievements_invalid_is_reached(session):

    response = session.get(
        ACHIEVEMENTS_URL,
        params={
            "is_reached": "invalid"
        }
    )

    assert response.status_code == 422

    data = response.json()

    check.equal(data["status"], "error")

    message_str = str(data["message"])

    check.is_in("bool_parsing", message_str)
    check.is_in("is_reached", message_str)
    check.is_in("Input should be a valid boolean", message_str)