# Contributing to aioitertools

## Preparation

You'll need to have Python 3.8 available for testing.
I recommend using [pyenv](https://github.com/pyenv/pyenv) for this:

```shell
pyenv install 3.8
pyenv shell 3.8
```

## Setup

Create a fresh development enviroment, and install the
appropriate tools and dependencies:

```shell
cd <path/to/aioitertools>
make venv
source .venv/bin/activate
```

## Submitting

Before submitting a pull request, please ensure
that you have done the following:

* Documented changes or features in README.md
* Added appropriate license headers to new files
* Written or modified tests for new functionality
* Used `make format` to format code appropriately
* Validated and tested code with `make lint test`
