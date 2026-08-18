.PHONY: help install test lint build clean deploy

help:
	@echo "Available targets: install, test, lint, build, clean, deploy"

install:
	pip install -e .[dev,full]

test:
	pytest tests/ -v --cov=sitejs --cov-report=term

lint:
	ruff check sitejs.py
	mypy sitejs.py

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache/ .coverage htmlcov/

deploy:
	twine upload dist/*
