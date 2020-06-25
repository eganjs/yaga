.PHONEY: lint fmt test

lint: .venv
	poetry run flake8
	poetry run isort --check-only --recursive .
	poetry run black --check --diff .

fmt: .venv
	poetry run isort --recursive .
	poetry run black .

test: .venv
	poetry run pytest --verbose --capture=no

.venv: poetry.lock
	poetry config virtualenvs.in-project true
	poetry install

poetry.lock: pyproject.toml
	poetry update
