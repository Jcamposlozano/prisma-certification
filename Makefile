SHELL := /bin/bash

.PHONY: install run test lint format docker-build docker-up docker-down docker-logs

install:
	poetry install

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .
	poetry run ruff check . --fix

docker-build:
	docker build -t certificate-service:latest .

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f
