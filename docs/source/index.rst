.. contents::

Welcome to openapi-SQLAlchemy's documentation!
==============================================

Translates openapi schemas to SQLAlchemy models to reduce duplication when
defining your API and database models. Any required additions to the openapi
specification are compliant with the openapi standard.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   technical_details/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Getting Started
===============

If you have the following openapi specification:

.. literalinclude:: ../../examples/simple-example-spec.yml

To use SQLAlchemy to retrieve *Employees* from a database you need the
following *models.py* file:

.. literalinclude:: ../../examples/simple_models.py

How Does It Work?
=================

Given a name for a schema, *openapi-SQLAlchemy* looks for that schema in the
schemas section of the specification. The schema must have the *x-tablename*
property which defines the name of the table. The schema is required to be an
*object*. For each *property* of the schema, a column is generated for the
table mapping openapi types to equivalent SQLAlchemy types.
