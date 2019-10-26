.. contents::

Welcome to OpenAPI-SQLAlchemy's documentation!
==============================================

Translates OpenAPI schemas to SQLAlchemy models to reduce duplication when
defining your API and database models. Any required additions to the OpenAPI
specification are compliant with the OpenAPI standard.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   examples/index
   technical_details/index


Getting Started
---------------

If you have the following OpenAPI specification:

.. literalinclude:: ../../examples/simple-example-spec.yml

To use SQLAlchemy to retrieve *Employees* from a database you need the
following *models.py* file:

.. literalinclude:: ../../examples/simple_models.py

How Does It Work?
-----------------

Given a name for a schema, *OpenAPI-SQLAlchemy* looks for that schema in the
schemas section of the specification. The schema must have the *x-tablename*
property which defines the name of the table. The schema is required to be an
*object*. For each *property* of the schema, a column is generated for the
table mapping OpenAPI types to equivalent SQLAlchemy types.
