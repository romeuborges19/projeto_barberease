FROM python:3.11

ENV PYTHONUNBUFFEED 1

RUN mkdir /barberease

WORKDIR /barberease

ADD . /barberease/

RUN pip install django

RUN pip install django-admin

RUN pip install python-decouple

RUN pip install psycopg

RUN pip install -r requirements.txt