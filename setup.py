"""Setup package."""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="OpenAPI-SQLAlchemy",
    version="0.7.0",
    author="David Andersson",
    author_email="anderssonpublic@gmail.com",
    description="Maps an OpenAPI schema to SQLAlchemy models.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/jdkandersson/OpenAPI-SQLAlchemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Database",
    ],
    python_requires=">=3.6",
    install_requires=["SQLAlchemy>=1.0", "typing-extensions>=3.5", "jsonschema>=3"],
    extras_require={
        "dev": [
            "pytest",
            "tox",
            "tox-pyenv",
            "pylint",
            "pytest-cov",
            "pytest-flakes",
            "pytest-flask",
            "pytest-flask-sqlalchemy",
            "mypy",
            "pydocstyle",
            "black",
            "pre-commit",
            "isort",
            "PyYAML",
            "Sphinx",
            "doc8",
            "connexion[swagger-ui]",
            "Flask-SQLAlchemy",
        ]
    },
)
