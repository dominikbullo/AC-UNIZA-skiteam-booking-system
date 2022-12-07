FROM python:3.7

# python envs
ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

COPY pyproject.toml /

RUN pip install --upgrade pip
RUN pip install poetry && poetry install

# upload scripts
COPY ./scripts/start.sh ./scripts/gunicorn.sh /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh &&\
    sed -i 's/\r$//g' /gunicorn.sh && chmod +x /gunicorn.sh
