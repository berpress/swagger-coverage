install:
	@poetry install

lint:
	@poetry run flake8 page_loader

build:
	@poetry build

publish:
	@poetry publish -r pypi_test

pytest:
	poetry run pytest