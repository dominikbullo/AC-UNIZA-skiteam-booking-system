#!/bin/sh

yes | python backend/manage.py makemigrations # This is a development thing so I don't have to run it manually, but will be removed in production
yes | python backend/manage.py migrate
yes | python backend/manage.py loaddata categories

python backend/manage.py runserver 0.0.0.0:8000 --settings=app.settings.dev
