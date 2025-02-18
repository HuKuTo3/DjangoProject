#!/bin/bash

echo "Applying database migration"
python manage.py makemigrations
python manage.py migrate

echo "Starting Gunicorn server"
gunicorn djangoProject.wsgi:application -c gunicorn.conf.py