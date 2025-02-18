#!/bin/bash

echo "Applying database migration"
python manage.py makemigrations
python manage.py migrate

echo "Starting Gunicorn server"
gunicorn django_project.wsgi:application -c gunicorn.conf.py