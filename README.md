# 🐉 PokemonBattle API Tests

Автоматизированный фреймворк для API-тестирования проекта **PokemonBattle**. Проект реализует проверку позитивных и негативных сценариев взаимодействия с сервером, валидацию схем ответов и интеграцию с CI/CD пайплайном.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-latest-brightgreen.svg)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Report-Allure-blueviolet.svg)](https://docs.qameta.io/allure/)
[![GitLab CI](https://img.shields.io/badge/GitLab-CI-orange.svg)](https://docs.gitlab.com/ee/ci/)

---

## 🛠️ Технологический стек

* **Язык:** Python 3.12
* **Фреймворк тестирования:** `pytest`, `pytest-check`
* **HTTP-клиент:** `requests` (кастомная обертка `ApiClient`)
* **Валидация данных:** `jsonschema`, `pydantic`
* **Отчетность:** `allure-pytest`
* **Управление окружением:** `python-dotenv`
* **Линтеры:** `ruff`, `flake8`, `pylint`
* **CI/CD:** GitLab CI/CD (с триггером на E2E Selenium-проекты)

---

## 📋 Предварительные требования

Перед началом работы убедитесь, что у вас установлены:
* Python 3.10 или выше
* Git
* (Опционально) Allure Commandline для генерации локальных отчетов

---

## 🚀 Установка и настройка

1. **Склонируйте репозиторий:**
 Создайте в корне проекта файл .env (скопируйте из .env.example, если он есть) и заполните его своими данными:
   ```bash
   git clone https://gitlab.qa.studio/python-auto-qa/workspaces/altair/UMBUT/pokemonbattle_api_tests.git
   cd pokemonbattle_api_tests

   BASE_URL=https://api.pokemonbattle.ru/v2
TRAINER_LOGIN=your_login@example.com
TRAINER_PASSWORD=your_password
TRAINER_TOKEN=your_api_token
TRAINER_ID=your_trainer_id
