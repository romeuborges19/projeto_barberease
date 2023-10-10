FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /barberease

WORKDIR /barberease

ADD . /barberease

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
