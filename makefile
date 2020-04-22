build:
	flit build

dev:
	flit install --symlink

setup:
	python -m pip install -Ur requirements-dev.txt

venv:
	python -m venv .venv
	source .venv/bin/activate && make setup dev
	echo 'run `source .venv/bin/activate` to use virtualenv'

release: lint test clean
	flit publish

format:
	python -m isort --apply --recursive aioitertools
	python -m black aioitertools

lint:
	python -m pylint --rcfile .pylint aioitertools
	python -m isort --diff --recursive aioitertools
	python -m black --check aioitertools

test:
	python -m coverage run -m aioitertools.tests
	python -m coverage report
	python -m mypy aioitertools

clean:
	rm -rf build dist README MANIFEST *.egg-info

distclean: clean
	rm -rf .venv