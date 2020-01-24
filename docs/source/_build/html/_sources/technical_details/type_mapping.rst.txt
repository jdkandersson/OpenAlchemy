Type Mapping
============

*OpenAlchemy* translates *OpenAPI* types to *SQLalchemy* types using the
following mappings:

+--------------+----------------+-----------------+-------------------+
| OpenAPI type | OpenAPI format | SQLAlchemy type | Python type       |
+==============+================+=================+===================+
| integer      | *undefined*    | Integer         | int               |
+--------------+----------------+-----------------+-------------------+
|              | int32          | Integer         | int               |
+--------------+----------------+-----------------+-------------------+
|              | int64          | BigInteger      | int               |
+--------------+----------------+-----------------+-------------------+
| number       | *undefined*    | Float           | float             |
+--------------+----------------+-----------------+-------------------+
|              | float          | Float           | float             |
+--------------+----------------+-----------------+-------------------+
| string       | *undefined*    | String          | str               |
+--------------+----------------+-----------------+-------------------+
|              | password       | String          | str               |
+--------------+----------------+-----------------+-------------------+
|              | byte           | String          | str               |
+--------------+----------------+-----------------+-------------------+
|              | binary         | LargeBinary     | bytes             |
+--------------+----------------+-----------------+-------------------+
|              | date           | Date            | datetime.date     |
+--------------+----------------+-----------------+-------------------+
|              | date-time      | DateTime        | datetime.datetime |
+--------------+----------------+-----------------+-------------------+
| boolean      |                | Boolean         | bool              |
+--------------+----------------+-----------------+-------------------+

String
------

*OpenAPI* optionally allows the *maxLength* property for *strings*. This is
translated to the *length* argument for the *SQLAlchemy* *String*, which is set
to *None* if *maxLength* is *undefined*.

Password
--------

The same *maxLength* information as for *String* also applies.

.. note:: The *password* format under the hood is the same as *String*. No
    special protection (such as encryption) is added.

Byte
------

This format is for *base64* encoded binary data. The same *maxLength*
information as for *String* also applies.

Binary
------

The same *maxLength* information as for *String* also applies. The codec is
assumed to be *utf-8*.

DateTime
--------

*OpenAPI* supports the inbuilt *date-time* format for a string. This is mapped
to the *DateTime* SQLAlchemy type. Currently, time zones are not supported.
Database best practice is to store everything in UTC. Applications, such as web
front ends, should convert to UTC as early as possible and localize a date and
time as late as possible.
