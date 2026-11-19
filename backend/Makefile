.PHONY: start test check-git-hooks format lint-fix lint-check

start:
	uv run fastapi dev src/main.py --port 3001

test:
	uv run pytest

check-git-hooks:
	cd .. && node .secret-scan/secret-scan.js -- --check-git-hooks

format: check-git-hooks
	uv run ruff format .

lint-fix: check-git-hooks
	-uv run ruff check --fix .
	uv run ruff format .

lint-check: check-git-hooks
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy
