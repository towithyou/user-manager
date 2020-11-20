#!/bin/bash
echo "start"
nginx
echo "start nginx"
sleep 40
python3 manage.py makemigrations
sleep 1
python3 manage.py migrate
sleep 2
python3 setup_data.py
sleep 2
exec python3 manage.py runserver 0.0.0.0:8000 --insecure

