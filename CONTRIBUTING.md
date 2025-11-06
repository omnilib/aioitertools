# Contributing to aioitertools

## Preparation

aioitertools uses [uv][] to manage environments and dependencies, and `make`
to run tests and linters.

You'll need to have Python 3.9 or newer available for testing:

```sh
$ uv python pin 3.14
```

## Testing

Run the test suite:

```shell-session
$ make test
```

Run the linters:

```shell-session
$ make lint
```

## Submitting

Before submitting a pull request, please ensure
that you have done the following:

* Documented changes or features in README.md
* Added appropriate license headers to new files
* Written or modified tests for new functionality
* Used `make format` to format code appropriately
* Validated and tested code with `make test lint`

[uv]: https://docs.astral.sh/uv/
