#!/bin/sh
python manage.py db migrate
python manage.py db upgrade

python manage.py runserver --host 0.0.0.0
