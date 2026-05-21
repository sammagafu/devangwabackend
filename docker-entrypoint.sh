#!/bin/sh
set -e

cd /app/devangwabackend

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
