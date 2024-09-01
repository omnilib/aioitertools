PKG:=aioitertools
EXTRAS:=dev,docs

UV_VERSION:=$(shell uv --version)
ifdef UV_VERSION
	VENV:=uv venv
	PIP:=uv pip
else
	VENV:=python -m venv
	PIP:=python -m pip
endif

.venv:
	$(VENV) .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to use virtualenv'

venv: .venv

install:
	$(PIP) install -Ue .[$(EXTRAS)]

release: lint test clean
	flit publish

format:
	python -m ufmt format $(PKG)

lint:
	python -m flake8 $(PKG)
	python -m ufmt check $(PKG)

test:
	python -m coverage run -m $(PKG).tests
	python -m coverage report
	python -m mypy -p $(PKG)

html: .venv README.md docs/*
	source .venv/bin/activate && sphinx-build -b html docs html

clean:
	rm -rf .mypy_cache build dist html README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv
