FROM python:3

RUN apt-get update
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common

WORKDIR /usr/src/app

COPY . .
RUN pip install -r requirements.txt

CMD [ "flask", "run" ]