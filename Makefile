install:
	@poetry install

lint:
	@pre-commit run --all-files

build:
	@poetry build

publish:
	@poetry publish

pytest:
	poetry run pytest
