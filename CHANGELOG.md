aioitertools
============

v0.6.1
------

Metadata fix

- Corrected description field for PyPI
- Switched from setuptools to flit for build/publish

```
$ git shortlog -s v0.6.0...v0.6.1
     1	Dima Tisnek
     5	John Reese
```


v0.6.0
------

Feature release v0.6.0

- First pieces of more_itertools (#18)

```
$ git shortlog -s v0.5.1...v0.6.0
     3	John Reese
     1	Zsolt Dollenstein
```


v0.5.1
------

Documentation Release v0.5.1

- Include changelog, code of conduct, and contributers guide in sdist
- Include wheels when building release distributions

```
$ git shortlog -s v0.5.0...v0.5.1
     4	John Reese
```


v0.5.0
------

Feature Release v0.5.0

- Feature: concurrency-limited implementation of asyncio.gather (#10)
- Fix: platform independent encoding in setup.py (#15, #16)
- Fix: make zip_longest stop iterating on finished iterators (#13)
- Improved documentation
- Overhaul package configuration and requirements
- Format package using isort
- Add coverage testing with codecov.io
- Switch to Github Actions for CI
- Testing on Python 3.8

```
$ git shortlog -s v0.4.0...v0.5.0
     1	Alexey Simuskov
    23	John Reese
     1	Tim Hatch
```


v0.4.0
------

Feature release v0.4.0

- Provisional module for friendly versions of the asyncio library.
  Access this via `aioitertools.asyncio`.

```
$ git shortlog -s v0.3.2...v0.4.0
     4	John Reese
```


v0.3.2
------

Bug fix release:

- chain.from_iterable now accepts async generators to provide iterables (#8)

```
$ git shortlog -s v0.3.1...v0.3.2
     1	A Connecticut Princess
     2	John Reese
```


v0.3.1
------

Bug fix release v0.3.1:

- Fixes `islice` consuming extra items (#7)

```
$ git shortlog -s v0.3.0...v0.3.1
     2	John Reese
     3	Vladimir Solomatin
```


v0.3.0
------

Feature release v0.3.0:

- Accept `start` parameter to `enumerate()` (#2)
- Added PEP 561 compliance and py.typed (#1)
- Support for functions that return awaitables (#5)

```
$ git shortlog -s v0.2.0...v0.3.0
     6	Bryan Forbes
    12	John Reese
```


v0.2.0
------

Feature release:

- Support all of itertools

```
$ git shortlog -s v0.1.0...v0.2.0
     8	John Reese
```


v0.1.0
------

Initial feature release:

- Shadow major builtins for iterables
- Unit tests for all builtins

```
$ git shortlog -s ce32bdb1777f84e8f64b9470d81b84b754389dd9...v0.1.0
     1	John Reese
```


