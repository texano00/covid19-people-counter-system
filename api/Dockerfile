FROM python:3

RUN apt-get update
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "run" ]