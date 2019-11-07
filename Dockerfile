FROM python:3.7-alpine
MAINTAINER Dominik Bullo

ENV PYTHONUNBUFFERED 1

#COPY ./requirements.txt /requirements.txt
#RUN pip install -r /requirements.txt
RUN pip install pipenv
COPY ./Pipfile /Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Crete folder on docker
RUN mkdir /app
WORKDIR /app

# Copy into docker
COPY ./app /app

# Create new user name user for security reasons
# -D runnig apps only
RUN adduser -D user
# Switch user to user
USER user
