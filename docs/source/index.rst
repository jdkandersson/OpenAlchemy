.. role:: python(code)
   :language: python

OpenAlchemy
===========

OpenAlchemy translates OpenAPI schemas to SQLAlchemy models to reduce
duplication when defining your API and database models. Any required additions
to the OpenAPI specification are compliant with the OpenAPI standard.

.. seealso::

   `Online Editor <https://editor.openalchemy.io/>`_
      Online editor including schema validation.

.. _getting-started:

Getting Started
---------------

If you have the following OpenAPI specification:

.. literalinclude:: ../../examples/simple/example-spec.yml
    :language: yaml
    :linenos:

To use SQLAlchemy to retrieve :samp:`Employees` from a database you need the
following :samp:`models.py` file:

.. literalinclude:: ../../examples/simple/models.py
    :language: python
    :linenos:

The :samp:`Base` for the SQLAlchemy models and the :samp:`Employee` model is
now available from :samp:`open_alchemy.models`::

    from open_alchemy.models import Base
    from open_alchemy.models import Employee

Interfaces
----------

The most user friendly interfaces are the :ref:`init-yaml` and
:ref:`init-json` interfaces. The :ref:`init-model-factory` interface is a
lower level interface which has fewer dependencies but is not as user
friendly.

.. _init-yaml:

:samp:`init_yaml`
^^^^^^^^^^^^^^^^^

Used to initialize the SQLAlchemy models based on a YAML OpenAPI specification
which has been extended with any relevant OpenAlchemy extension properties.

The :samp:`init_yaml` interface requires the :samp:`PyYAML` library to be
installed. The :samp:`init_yaml` interface accepts the following arguments:

* :samp:`spec_filename`: The name of the file as a positional argument. The
  file must by a YAML file.
* :samp:`base`: The SQLAlchemy declarative base as an optional keyword only
  argument. It is used to as the base class for all SQLAlchemy models. If it
  is not passed in, a new declarative base is constructed.
* :samp:`models_filename`: The name of the file where the SQLAlchemy models
  will be written as an optional keyword only argument.
* :samp:`spec_path`: The path to the OpenAPI specification (what would need to
  be passed to the :samp:`open` function to read the file) as an optional
  keyword only argument. Used to support remote references.

.. note:: the :samp:`define_all` parameter has been removed and OpenAlchemy
  behaves as though it is set to :samp:`True`.

The return value is a tuple consisting of:

* :samp:`Base`: The SQLAlchemy declarative based used for the models. It is
  also importable: :python:`from open_alchemy.models import Base`.
* :samp:`model_factory`: The factory that can be used to construct the
  SQLAlchemy models using the name of the schema in the OpenAPI specification.
  All constructed models are added to the :samp:`open_alchemy.models` module
  and are importable. For example:
  :python:`from open_alchemy.models import Employee`.

.. _init-json:

:samp:`init_json`
^^^^^^^^^^^^^^^^^

The :samp:`init_json` interface is similar to the :ref:`init-yaml` interface
except that :samp:`spec_filename` must be a JSON file and :samp:`PyYAML` is not
a required dependency.

:samp:`build_yaml`
^^^^^^^^^^^^^^^^^^

Used to build a package with the SQLAlchemy models (including type hints) based
on a YAML OpenAPI specification which has been extended with any relevant
OpenAlchemy extension properties.

To build models from the command line, run::

  openalchemy build openapi.yml simple dist

This interface is described in details in the :ref:`build-yaml` section of the
Advanced chapter.


.. _build-json:

:samp:`build_json`
^^^^^^^^^^^^^^^^^^

The :samp:`build_json` interface is similar to the :ref:`build-yaml` interface
except that :samp:`spec_filename` must be a JSON file and :samp:`PyYAML` is not
a required dependency.

Models File
-----------

Optionally, model definitions can be persisted to disk, mainly for type hinting
and IDE auto-completion.

To discover the internal details of the models file, refer to the
:ref:`models-file` section in the Advanced chapter.

.. _alembic:

Alembic
-------

The standard method for automatically generating database migrations for
alembic is supported. The following instructions show how to get started:

.. literalinclude:: ../../examples/alembic/readme.md
    :language: md


How Does It Work?
-----------------

Helped by a series of extension properties, OpenAlchemy turns
`OpenAPI schemas <https://swagger.io/specification/#schema-object>`_
into SQL entities.

To understand how all this works under the hood, refer to
:ref:`how-does-it-work` section in the Advanced chapter.


Table of Content
----------------

.. toctree::
  :caption: GENERAL
  :maxdepth: 1

  technical_details/index
  examples/index
  cli
  advanced
  package_service
  CHANGELOG

.. toctree::
  :caption: DEVELOPMENT
  :maxdepth: 1

  CONTRIBUTING
