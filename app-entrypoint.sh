#!/bin/sh
# Migrate DB
python manage.py db stamp head
python manage.py db migrate
python manage.py db upgrade

source env/bin/activate

python3 manage.py runserver --host 0.0.0.0