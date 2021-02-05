#!/bin/bash

python manage.py db stamp head
python manage.py db migrate
python manage.py db upgrade
pip install pyyaml
python import_script.py
