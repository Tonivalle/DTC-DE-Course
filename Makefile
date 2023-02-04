.PHONY: serve
serve:
	mkdocs serve 

.PHONY: docs-deploy
docs-deploy:
	./code/utils/auto_build_docs.sh