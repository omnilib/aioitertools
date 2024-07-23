PKG:=aioitertools
EXTRAS:=dev,docs

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to use virtualenv'

venv: .venv

install:
	python -m pip install -Ue .[$(EXTRAS)]

release: lint test clean
	flit publish

format:
	python -m ufmt format $(PKG)

lint:
	python -m flake8 $(PKG)
	python -m mypy -p $(PKG)
	python -m ufmt check $(PKG)

test: lint
	python -m coverage run -m $(PKG).tests
	python -m coverage report

html: .venv README.md docs/*
	source .venv/bin/activate && sphinx-build -b html docs html

clean:
	rm -rf .mypy_cache build dist html README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv
