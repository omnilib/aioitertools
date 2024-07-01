PKG:=aioitertools
EXTRAS:=dev,docs

venv:
	poetry shell

install:
	poetry install --with $(EXTRAS)

release: lint test clean
	poetry publish

format:
	python -m ufmt format $(PKG)

lint:
	python -m flake8 $(PKG)
	python -m ufmt check $(PKG)

test:
	python -m coverage run -m $(PKG).tests
	python -m coverage report
	python -m mypy -p $(PKG)

docs-html: venv README.md docs/*
	sphinx-build -b html docs html

clean:
	rm -rf .mypy_cache build dist html README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv
