install:
	@poetry install

lint:
	@pre-commit run --all-files

build:
	@poetry build

publish:
	@poetry publish -r pypi_test

pytest:
	poetry run pytest
