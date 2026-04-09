SHELL := /bin/bash

.PHONY: install run test lint format docker-build docker-up docker-down docker-logs

install:
\tpoetry install

run:
\tpoetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
\tpoetry run pytest

lint:
\tpoetry run ruff check .

format:
\tpoetry run ruff format .
\tpoetry run ruff check . --fix

docker-build:
\tdocker build -t certificate-service:latest .

docker-up:
\tdocker compose up --build

docker-down:
\tdocker compose down -v

docker-logs:
\tdocker compose logs -f
