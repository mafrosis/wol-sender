.PHONY: lint
lint:
	docker compose run --rm --entrypoint=pylint test /src/wol_sender

.PHONY: typecheck
typecheck:
	docker compose run --rm test --mypy /src/wol_sender

.PHONY: dist
dist:
	pip install wheel build
	python -m build
