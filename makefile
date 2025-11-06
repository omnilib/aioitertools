PKG:=aioitertools

all: format test lint

format:
	uv run ufmt format $(PKG)

lint:
	uv run ruff check $(PKG)
	uv run ufmt check $(PKG)

fix:
	uv run ruff check --fix --unsafe-fixes $(PKG)

test:
	uv run coverage run -m $(PKG).tests
	uv run coverage report
	uv run mypy -p $(PKG)

html: .venv README.md docs/*
	uv run --group docs sphinx-build -b html docs html

clean:
	rm -rf .mypy_cache uv.lock build dist html README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv
