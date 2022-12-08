FROM python:3.7

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1


WORKDIR /app/backend

# Upload Poetry files
COPY pyproject.toml poetry.lock ./

# Upgrage pip, install poetry and install packpages (also creates virtual env)
RUN pip install --upgrade pip
RUN pip install poetry && poetry install
