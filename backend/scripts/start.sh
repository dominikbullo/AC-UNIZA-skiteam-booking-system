#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

poetry install
poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput --clear --verbosity 0
poetry run python manage.py runserver_plus 0.0.0.0:8000
