build:
	python3 setup.py build

dev:
	python3 setup.py develop

setup:
	pip3 install -U black mypy pylint twine

venv:
	python3 -m venv .venv
	source .venv/bin/activate && make setup dev
	echo 'run `source .venv/bin/activate` to use virtualenv'

release: lint test clean
	python3 setup.py sdist
	python3 -m twine upload dist/*

black:
	black aioitertools setup.py

lint:
	-mypy --ignore-missing-imports --python-version 3.6 .
	pylint --rcfile .pylint aioitertools setup.py
	black --check aioitertools setup.py

test:
	python3 -m unittest -v aioitertools.tests

clean:
	rm -rf build dist README MANIFEST *.egg-info
