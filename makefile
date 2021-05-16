build:
	flit build

dev:
	flit install --symlink

setup:
	python -m pip install -Ur requirements-dev.txt

.venv:
	python -m venv .venv
	source .venv/bin/activate && make setup dev
	echo 'run `source .venv/bin/activate` to use virtualenv'

venv: .venv

release: lint test clean
	flit publish

format:
	python -m usort format aioitertools
	python -m black aioitertools

lint:
	python -m flake8 aioitertools
	python -m usort check aioitertools
	python -m black --check aioitertools

test:
	python -m coverage run -m aioitertools.tests
	python -m coverage report
	python -m mypy aioitertools

html: .venv README.md docs/*
	source .venv/bin/activate && sphinx-build -b html docs html

clean:
	rm -rf build dist html README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv