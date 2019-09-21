"""Setup package."""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="openapi-SQLAlchemy",
    version="0.4.0",
    author="David Andersson",
    author_email="anderssonpublic@gmail.com",
    description="Maps an openapi schema to SQLAlchemy models.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/jdkandersson/openapi-SQLAlchemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Database",
    ],
    python_requires=">=3.7",
    install_requires=["SQLAlchemy>=1.3.6", "typing-extensions>=3.7.4"],
    extras_require={
        "dev": [
            "pytest",
            "tox",
            "pylint",
            "pytest-cov",
            "pytest-flakes",
            "mypy",
            "pydocstyle",
            "black",
            "pre-commit",
            "isort",
            "PyYAML",
            "Sphinx",
            "doc8",
        ]
    },
)
