import json

import allure
import pytest

from utils.helpers import TRAINERS_URL, TRAINER_ID


@allure.title("GET /trainers: получение тренеров по городу")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.positive
def test_get_trainers_by_city(session):
    city = "Москва"

    allure.attach(
        city,
        name="Фильтр по городу",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("Отправляем GET-запрос с фильтром по городу"):
        response = session.get(TRAINERS_URL, params={"city": city})

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step("Проверяем, что все тренеры из указанного города"):
        data = response.json()["data"]
        assert len(data) > 0, "Список тренеров не должен быть пустым"

        for trainer in data:
            assert trainer["city"].lower() == city.lower()


@allure.title("GET /trainers: получение тренера по ID")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skip(reason="Пример пропуска теста")
def test_get_trainer_by_id(session):
    allure.attach(
        str(TRAINER_ID),
        name="ID тренера",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("Отправляем GET-запрос с параметром trainer_id"):
        response = session.get(TRAINERS_URL, params={"trainer_id": TRAINER_ID})

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step("Проверяем, что вернулся ровно один тренер с нужным ID"):
        data = response.json()["data"]
        assert len(data) == 1
        assert int(data[0]["id"]) == TRAINER_ID


@allure.title("GET /trainers: получение тренеров по городу с сортировкой desc_level")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.positive
def test_get_trainers_by_city_sorted_desc(session):
    city = "Москва"

    allure.attach(
        json.dumps({"city": city, "sort": "desc_level"}, indent=2, ensure_ascii=False),
        name="Параметры запроса",
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Отправляем GET-запрос с фильтром по городу и сортировкой по уровню"):
        response = session.get(
            TRAINERS_URL,
            params={"city": city, "sort": "desc_level"},
        )

    with allure.step("Проверяем, что статус-код ответа 200"):
        assert response.status_code == 200

    with allure.step("Проверяем, что все тренеры из указанного города"):
        data = response.json()["data"]
        assert len(data) > 0, "Список тренеров не должен быть пустым"

        for trainer in data:
            assert trainer["city"].lower() == city.lower()

    with allure.step("Проверяем, что уровни тренеров отсортированы по убыванию"):
        levels = [int(trainer["level"]) for trainer in data]
        assert levels == sorted(levels, reverse=True)