SRC_DIR = code
PYTEST_FLAGS = -vv tests

.PHONY: format
format:
	poetry run black $(SRC_DIR)
	poetry run isort $(SRC_DIR)

.PHONY: format-check
format-check:
	poetry run black --check $(SRC_DIR)
	poetry run isort --check $(SRC_DIR)

.PHONY: check
check: format-check lint type-check 

.PHONY: lint
lint: 
	poetry run pylint -j 0 $(SRC_DIR) -d missing-function-docstring -d missing-class-docstring

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
	./code/utils/auto_build_docs.sh