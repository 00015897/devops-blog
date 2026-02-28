#!/bin/bash
set -e

cd /srv/devops_blog

docker compose pull
docker compose up -d
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput

