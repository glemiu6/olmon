.PHONY: install style_check

install:
	uv sync

style_check:
	uv run ruff format olmon/
	uv run ruff check olmon/
	uv run mypy olmon/