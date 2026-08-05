import pytest
import requests

TOKEN = "8f36a308c11872d3941dd3c906f19b16"


@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    session.headers.update({
        "trainer_token": TOKEN
    })
    return session