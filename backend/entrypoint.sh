#!/bin/sh

mkdir -p /app/static /app/staticfiles

chown -R nonroot:nonroot /app/static /app/staticfiles
chmod -R 755 /app/static /app/staticfiles

while ! nc -z "db" ${DB_PORT:-5432}; do
  sleep 0.5
done

echo "PostgreSQL started"

python manage.py compilescss
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata fixtures/user/users.json
python manage.py loaddata fixtures/polls/polls_Category.json
python manage.py loaddata fixtures/polls/polls_Question.json
python manage.py loaddata fixtures/polls/polls_Choice.json

exec "$@"