#!/bin/sh
set -e

echo "PostgreSQL is ready!"

echo "Applying database migrations..."
python manage.py migrate --noinput
  
python manage.py compilescss
python manage.py collectstatic --noinput

exec "$@"