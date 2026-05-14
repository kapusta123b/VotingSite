#!/bin/sh
set -e

while ! nc -z db ${DB_PORT:-5432}; do
  sleep 0.5
done

echo "PostgreSQL started"

python manage.py compilescss
python manage.py collectstatic --noinput
python manage.py migrate

exec "$@"