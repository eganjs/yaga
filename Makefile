.PHONEY: lint fmt test

lint:
	poetry run flake8
	poetry run isort --check-only --recursive .
	poetry run black --check .

fmt:
	poetry run isort --recursive .
	poetry run black .

test:
	poetry run pytest --verbose --capture=no
