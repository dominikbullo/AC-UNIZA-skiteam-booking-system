FROM python:3.7-alpine
LABEL maintainer="dominobullo@gmail.com"

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## Copy into docker
RUN mkdir /app
WORKDIR /app

COPY backend/Pipfile* /

# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Pillow
# https://stackoverflow.com/questions/57787424/django-docker-python-unable-to-install-pillow-on-python-alpine
RUN apk update \
    && apk add --no-cache jpeg-dev zlib-dev \
    && apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

#Instal also dev packpages
RUN pipenv lock --dev --requirements > requirements_dev.txt
RUN pip install -r requirements_dev.txt

COPY . /app
EXPOSE 8000

## Create new user name user for security reasons
## -D runnig apps only
#RUN adduser -D user
## Switch user to user
#USER user
