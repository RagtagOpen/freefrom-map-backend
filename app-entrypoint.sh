#!/bin/sh
python manage.py db stamp head
python manage.py db migrate
python manage.py db upgrade

python import_script.py

python manage.py runserver --host 0.0.0.0
