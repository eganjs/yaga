.PHONEY: lint fmt test

lint: .venv
	poetry run flake8 --exclude .venv
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
	@touch .venv

poetry.lock: pyproject.toml
	poetry update
	@touch poetry.lock
