import allure
import pytest
import requests

from utils.api_client import ApiClient
from utils.constants import BASE_URL
from utils.helpers import create_pokemon

TOKEN = "8f36a308c11872d3941dd3c906f19b16"


@pytest.fixture(scope="session")
def session():
    """Клиент для запросов к API: сессия с токеном тренера,
    все вызовы логируются в allure."""
    with allure.step("Создаём сессию API с токеном тренера"):
        raw_session = requests.Session()
        raw_session.headers.update({"trainer_token": TOKEN})
        client = ApiClient(base_url=BASE_URL, session=raw_session)

    yield client

    # Закрываем сессию ПОСЛЕ всех тестов
    raw_session.close()


@pytest.fixture
def pokemon_created(session):
    """Создаёт покемона до теста и отдаёт его id."""
    with allure.step("Создаём тестового покемона для теста"):
        pokemon_id = create_pokemon(session)

    yield pokemon_id