Async REST API for a restaurant menu

Запуск приложения:
 - клонируем репозиторий
 - переходим в папку с проектом
 - создаем виртуальное окружение и активируем его:
    ```python -m venv .venv```
    ```source .venv/bin/activate``
 - устанавливаем зависимости:
    ```pip install -r ./requirements.txt```
 - поднимаем базу данных:
    ```docker-compose -f docker-compose.yaml up -d```
 - запускаем миграции:
    ```alembic upgrade heads```
 - запускаем приложение:
    ```uvicorn app.main:app --reload```

Документация доступна по адресу http://127.0.0.1:8000/docs