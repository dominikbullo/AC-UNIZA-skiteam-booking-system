#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

poetry install
poetry run manage.py migrate
poetry run manage.py collectstatic --noinput --verbosity 0
poetry run gunicorn config.wsgi -w 4 --worker-class gevent -b 0.0.0.0:8000 --chdir=/app
