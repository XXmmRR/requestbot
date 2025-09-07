#!/bin/bash
set -e

# Переходим в главную рабочую директорию
cd /app

# Добавляем текущую директорию в путь поиска модулей Python
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Ожидаем, пока база данных станет доступной
echo "Ожидаю готовности базы данных..."
until nc -z $DB_HOST $DB_PORT; do
  echo "База данных пока недоступна. Жду 1 секунду..."
  sleep 1
done
echo "База данных готова!"

# Выполняем миграции Alembic, указывая путь к его конфигурационному файлу
echo "Запускаю миграции Alembic..."
uv run alembic -c database/alembic.ini upgrade head

# Запускаем основное приложение
echo "Запускаю основное приложение..."
uv run "$@"
