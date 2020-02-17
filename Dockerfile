FROM python:3.6
RUN apt update
RUN apt-get install  postgresql-contrib -y
RUN apt-get install musl-dev -y
RUN apt-get install libpq-dev gcc
RUN apt-get install python3-dev -y
RUN export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH
RUN pip3 install psycopg2-binary
RUN pip3 install psycopg2
RUN pip3 install djangorestframework
RUN pip3 install markdown
RUN pip3 install django-filter
RUN apt-get install -y binutils libproj-dev gdal-bin

# Delete build dependencies 
# RUN apk del .build-deps

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/