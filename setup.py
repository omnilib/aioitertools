from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("aioitertools/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split('"')[1]

setup(
    name="aioitertools",
    description="asyncio version of the standard multiprocessing module",
    long_description=readme,
    long_description_content_type="text/markdown",
    version=version,
    author="John Reese",
    author_email="john@noswap.com",
    url="https://github.com/jreese/aioitertools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
    packages=["aioitertools", "aioitertools.tests"],
    package_data={"aioitertools": ["py.typed"]},
    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
    install_requires=[],
)
