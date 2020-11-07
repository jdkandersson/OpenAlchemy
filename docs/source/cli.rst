OpenAlchemy CLI
===============

openalchemy build
-----------------

Description
^^^^^^^^^^^

Build a Python package containing the models described in the OpenAPI
specification file.

Usage
^^^^^

.. program:: openalchemy

.. option:: openalchemy build [OPTIONS] SPECFILE PKG_NAME OUTPUT_DIR


Extended Description
^^^^^^^^^^^^^^^^^^^^

The :samp:`openalchemy build` command builds a reusable Python package based off
of the specification file.

For instance, running the following command::

  openalchemy build openapi.yml simple dist

Produces the following artifacts::

  dist
  └── simple
      ├── MANIFEST.in
      ├── build
      ├── dist
      │   ├── simple-0.1-py3-none-any.whl
      │   └── simple-0.1.tar.gz
      ├── setup.py
      ├── simple
      │   ├── __init__.py
      │   └── spec.json
      └── simple.egg-info

By default, a source and a wheel package are built, but this behavior can be
adjusted by using the :samp:`--format` option.

Options
^^^^^^^

+-----------------+--------------+-------------------------------------------+
| Name, shorthand | Default      | Description                               |
+-----------------+--------------+-------------------------------------------+
| --format, -f    | sdist, wheel | limit the format to either sdist or wheel |
+-----------------+--------------+-------------------------------------------+

openalchemy generate
---------------------

Description
^^^^^^^^^^^

Generate the models described in the OpenAPI specification file.

Usage
^^^^^

.. program:: openalchemy

.. option:: openalchemy generate SPECFILE OUTPUT_FILE


Extended Description
^^^^^^^^^^^^^^^^^^^^

The :samp:`openalchemy generate` command generates the models without having to
start an application.

Example::

  openalchemy generate openapi.yml models.py
