FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /barberease

WORKDIR /barberease

ADD . /barberease

RUN pip install -r requirements.txt


CMD python manage.py migrate && gunicorn --bind :8000 --workers 3barberease.wsgi:application
