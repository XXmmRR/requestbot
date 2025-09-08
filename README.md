
-----

### 🚀 Запуск проекта

Этот проект использует **Docker Compose** для запуска всех необходимых сервисов: бота, базы данных PostgreSQL и кэша Redis.

-----

### 📋 Требования

  * **Docker** и **Docker Compose** должны быть установлены на вашем компьютере.

-----

### 🛠️ Настройка

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/your-username/RequestBot.git
    cd RequestBot
    ```

2.  **Настройте переменные окружения:**
    Создайте файл `.env` в корневой директории проекта и заполните его, используя следующий шаблон.

    ```ini
    # .env
    TOKEN=your_telegram_bot_token
    ADMIN=your_telegram_user_id
    POSTGRES_DB=your_database_name
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    DB_HOST=db
    DB_PORT=5432
    ```

-----

### 📦 Запуск сервисов

Чтобы запустить все сервисы в фоновом режиме, выполните:

```bash
docker-compose up -d --build
```

-----

### 🏗️ Работа с миграциями базы данных

Для управления схемой базы данных используется **Alembic**. Все команды Alembic должны выполняться **внутри контейнера `bot`**.

1.  **Создание новой миграции:**

    ```bash
    docker-compose run --rm bot alembic -c database/alembic.ini revision --autogenerate -m "Описание изменений"
    ```

2.  **Применение миграций:**

    ```bash
    docker-compose run --rm bot alembic upgrade head
    ```

-----

### 🛑 Остановка сервисов

Чтобы остановить все контейнеры, используйте:

```bash
docker-compose down
```