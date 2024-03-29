JSON
====

SQLAlchemy supports generic JSON data for some databases. A property can be
marked as JSON using the :samp:`x-json` extension property.

.. seealso::

    :ref:`x-json`
      OpenAlchemy documentation for the :samp:`x-json` extension property.

    `SQLAlchemy JSON <https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.JSON>`_
      Documentation for the SQLAlchemy JSON type.

The following example defines the :samp:`data` property of :samp:`Employee` to
be generic JSON data:

.. literalinclude:: ../../../examples/json/example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../examples/json/models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../examples/json/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../examples/json/models_auto.py
    :language: python
    :linenos:

.. seealso::
    :ref:`getting-started`
