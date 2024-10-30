# Conference App

## Установка

1. Клонируйте репозиторий:
   ```bash
    git clone <repository-url>
    cd conference_app
   ```
2. Установите переменные среды:
   ```
    POSTGRES_SERVER=db
    POSTGRES_PORT=5432
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=conference_db

    # Заполнять БД данными?
    INSERT_DATA_MODE=True
    ```
3. Запустите приложение:
   ```bash
    docker-compose up --build
   ```

4. Документация Swagger доступна по адресу
    <http://localhost:8002/docs>

5. Запуск тестирования (могут портебоваться изменения вида импортов внутри database.py, conftest.py, main.py)
   ```bash
    pytest -v
   ```
