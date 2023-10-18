python manage.py migrate --noinput
gunicorn --bind :8000 --workers 3 barberease.wsgi:application
