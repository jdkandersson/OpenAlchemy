"""Setup package."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-SQLAlchemy",
    version="0.0.1",
    author="David Andersson",
    author_email="anderssonpublic@gmail.com",
    description="Maps an openapi schema to SQLAlchemy models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jdkandersson/openapi-SQLAlchemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Topic :: Database",
    ],
)
