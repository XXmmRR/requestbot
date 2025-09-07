#!/bin/bash
set -e

echo "Ожидаю готовности базы данных..."
until nc -z $DB_HOST $DB_PORT; do
  echo "База данных пока недоступна. Жду 1 секунду..."
  sleep 1
done
echo "База данных готова!"

echo "Запускаю миграции Alembic..."
alembic upgrade head

echo "Запускаю основное приложение..."
exec "$@"
