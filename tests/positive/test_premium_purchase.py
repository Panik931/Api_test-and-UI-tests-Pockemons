import copy
import time
import json

import allure
import pytest


VALID_PREMIUM_PAYLOAD = {
    "order_type": "premium",
    "details": {
        "days": 12,
        "card_number": "5555555544444442",
        "card_name": "german dolnikov",
        "card_actual": "10/27",
        "card_cvv": "125",
        "secure_code": "56456",
    },
}

@pytest.mark.api
@pytest.fixture
def premium_purchased(lavka_session):
    """Покупает Premium до теста и отменяет подписку после,
    чтобы вернуть систему в исходное состояние."""
    with allure.step("Сбрасываем состояние: отменяем премиум, если активен"):
        lavka_session.post("/cancel_premium")

    with allure.step("Покупаем Premium с валидными данными карты"):
        response = lavka_session.post(
            "/payments",
            json=copy.deepcopy(VALID_PREMIUM_PAYLOAD),
        )
        assert response.status_code == 200, response.text

    yield response.json()

    with allure.step("Отменяем подписку Premium (возврат в исходное состояние)"):
        cancel = lavka_session.post("/cancel_premium")
        assert cancel.status_code == 200, cancel.text


@allure.title("E2E: успешная покупка Premium (happy path)")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive
def test_buy_premium_happy_path(lavka_session, premium_purchased):
    purchase = premium_purchased

    with allure.step("Проверяем, что транзакция успешна и дни начислены"):
        assert purchase["message"] == "Транзакция успешна"
        assert purchase["days"] == VALID_PREMIUM_PAYLOAD["details"]["days"]

    with allure.step("Проверяем, что в истории есть успешная premium-транзакция"):
        response = lavka_session.get("/payments")
        assert response.status_code == 200, response.text
        history = response.json()["data"]
        premium_ops = [
            op for op in history if op["order_type"] == "premium"
        ]
        assert premium_ops, "История не содержит premium-покупок"
        assert int(premium_ops[0]["details"]["status"]) == 1


@allure.title("E2E: платёж не прошёл — невалидные данные в запросе /payments")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("card_number", "4242424242424241"),  # не проходит проверку Луна
        ("secure_code", "123"),               # неверный 3DS-код
        ("card_actual", "10/40"),             # срок действия дальше 2035 года
        ("card_number", "DELETE"),            # отсутствует номер карты
        ("card_cvv", "DELETE"),               # отсутствует CVV
        ("days", "DELETE"),                   # отсутствует количество дней
    ],
)
def test_buy_premium_payment_failed(lavka_session, field, bad_value):
    # Пауза, чтобы не упереться в лимит запросов Лавки на /payments
    time.sleep(20)

    payload = copy.deepcopy(VALID_PREMIUM_PAYLOAD)

    with allure.step(f"Ломаем поле '{field}' в теле запроса"):
        if bad_value == "DELETE":
            del payload["details"][field]
        else:
            payload["details"][field] = bad_value

    with allure.step("Отправляем запрос на покупку Premium"):
        response = lavka_session.post("/payments", json=payload)

    # Страховка: если платёж вдруг прошёл — отменяем покупку
    if response.status_code == 200:
        lavka_session.post("/cancel_premium")

    with allure.step("Проверяем, что платёж не прошёл (400 или 422)"):
        assert response.status_code in (400, 422), response.text
        assert response.json()["status"] == "error"

@allure.title("E2E: платёж не прошёл — нет денег на карте")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_buy_premium_payment_declined(lavka_session):
    payload = copy.deepcopy(VALID_PREMIUM_PAYLOAD)

    with allure.step("Устанавливаем cvv=300 — карта без денег"):
        payload["details"]["card_cvv"] = "300"

    with allure.step("Отправляем запрос на покупку Premium"):
        response = lavka_session.post("/payments", json=payload)

    # Страховка: если платёж вдруг прошёл — отменяем покупку
    if response.status_code == 200:
        lavka_session.post("/cancel_premium")

    with allure.step("Проверяем, что платёж отклонён с ошибкой 'нет денег на карте'"):
        assert response.status_code in (400, 422), response.text
        body = response.json()

        allure.attach(
            json.dumps(body, indent=2, ensure_ascii=False),
            name="Ответ платежа",
            attachment_type=allure.attachment_type.JSON,
        )

        assert body["status"] == "error"
        assert "недостаточно средств" in body["message"].lower()