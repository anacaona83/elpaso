#!/bin/bash

NAME="elpaso_app"
DJANGODIR=/home/%USER/python/elpaso

#SOCKFILE=/home/%USER/python/elpaso/run/gunicorn.sock
USER=%USER
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=elpaso.settings
DJANGO_WSGI_MODULE=elpaso.wsgi

echo "Starting $NAME"

# Activate the virtual env
source /home/%USER/python/envs/env_elpaso/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --log-level=debug \
  --bind=62.210.239.81:8443