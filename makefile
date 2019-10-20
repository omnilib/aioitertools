build:
	python setup.py build

dev:
	python setup.py develop

setup:
	python -m pip install -Ur requirements-dev.txt

venv:
	python -m venv .venv
	source .venv/bin/activate && make setup dev
	echo 'run `source .venv/bin/activate` to use virtualenv'

release: lint test clean
	python setup.py sdist
	python -m twine upload dist/*

format:
	python -m isort --apply --recursive aioitertools setup.py
	python -m black aioitertools setup.py

lint:
	python -m pylint --rcfile .pylint aioitertools setup.py
	python -m isort --diff --recursive aioitertools setup.py
	python -m black --check aioitertools setup.py

test:
	python -m coverage run -m aioitertools.tests
	python -m coverage report
	python -m mypy aioitertools

clean:
	rm -rf build dist README MANIFEST *.egg-info
