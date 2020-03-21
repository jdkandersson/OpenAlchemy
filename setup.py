"""Setup package."""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="OpenAlchemy",
    version="1.0.0",
    author="David Andersson",
    author_email="anderssonpublic@gmail.com",
    description="Maps an OpenAPI schema to SQLAlchemy models.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/jdkandersson/OpenAlchemy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet",
        "Typing :: Typed",
    ],
    python_requires=">=3.6",
    install_requires=["SQLAlchemy>=1.0", "jsonschema>=3", "Jinja2>=2", "black"],
    include_package_data=True,
    extras_require={
        "yaml": ["PyYAML"],
        "dev": [
            "tox",
            "tox-pyenv",
            "pylint",
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
            "alembic",
        ],
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-flake8",
            "pytest-flask",
            "pytest-flask-sqlalchemy",
            "pytest-randomly",
            "pytest-bandit",
            "PyYAML",
            "connexion[swagger-ui]",
            "typeguard",
        ],
        ":python_version<'3.7'": [
            "dataclasses>=0.7",
            "backports-datetime-fromisoformat>=1.0.0",
        ],
        ":python_version<'3.8'": ["typing_extensions>=3.7.4"],
    },
)
