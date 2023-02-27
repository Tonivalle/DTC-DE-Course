SRC_DIR = src/dtc_de_course
PYTEST_FLAGS = -vv tests

.PHONY: format
format:
	poetry run black $(SRC_DIR)
	poetry run isort $(SRC_DIR) --profile black

.PHONY: format-check
format-check:
	poetry run black --check $(SRC_DIR)
	poetry run isort --check $(SRC_DIR) --profile black

.PHONY: check
check: format-check lint type-check 

.PHONY: lint
lint: 
	poetry run pylint -j 0 $(SRC_DIR) -d missing-function-docstring -d missing-class-docstring -d missing-module-docstring

.PHONY: test
test:
	poetry run pytest $(PYTEST_FLAGS)

.PHONY: type-check
type-check:
	poetry run mypy --ignore-missing-imports $(SRC_DIR)

.PHONY: serve
serve:
	mkdocs serve 

.PHONY: docs-deploy
docs-deploy:
	./src/dtc_de_course/utils/auto_build_docs.sh