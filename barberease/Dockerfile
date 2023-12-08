FROM python:3.11

# Configurações do python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Organizando a pasta
RUN mkdir /barberease

WORKDIR /barberease

ADD . /barberease

#Instalando dependências
RUN pip install -r requirements.txt

# Rodando o projeto
CMD python manage.py collectstatic --no-input && python manage.py migrate && gunicorn --bind :8000 --workers 3 barberease.wsgi:application

