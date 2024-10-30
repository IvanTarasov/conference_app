FROM python:3.12

RUN apt-get update

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --no-dev

COPY . .

EXPOSE 8002