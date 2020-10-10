"""Setup package."""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="OpenAlchemy",
    version="1.6.0",
    author="David Andersson",
    author_email="anderssonpublic@gmail.com",
    description="Maps an OpenAPI schema to SQLAlchemy models.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/jdkandersson/OpenAlchemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "SQLAlchemy>=1.0",
        "jsonschema>=3",
        "Jinja2>=2",
        "sqlalchemy-stubs>=0.3",
    ],
    include_package_data=True,
    extras_require={
        "yaml": ["PyYAML"],
        "wheel": ["wheel"],
        "dev": [
            "tox",
            "tox-pyenv",
            "pylint",
            "mypy",
            "pydocstyle",
            "black",
            "pre-commit",
            "isort<5.0.0",
            "Sphinx",
            "doc8",
            "connexion[swagger-ui]",
            "Flask-SQLAlchemy",
            "alembic",
        ],
        "test": [
            "bandit",
            "pytest",
            "pytest-cov",
            "pytest-flake8",
            "pytest-flask",
            "pytest-flask-sqlalchemy",
            "pytest-randomly",
            "PyYAML",
            "connexion[swagger-ui]",
            "typeguard",
            "sqlalchemy_mixins",
            "wheel",
        ],
        ":python_version<'3.8'": ["typing_extensions>=3.7.4"],
    },
)
