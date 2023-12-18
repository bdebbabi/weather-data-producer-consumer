FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN pip install poetry
COPY poetry.lock pyproject.toml  opt/

RUN cd opt/ && poetry config virtualenvs.create false && poetry install

COPY src opt/src
COPY .env .env