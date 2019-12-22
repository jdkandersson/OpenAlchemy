Type Mapping
============

*OpenAlchemy* translates *OpenAPI* types to *SQLalchemy* types using the
following mappings:

+--------------+----------------+-----------------+
| OpenAPI type | OpenAPI format | SQLAlchemy type |
+==============+================+=================+
| integer      | *undefined*    | Integer         |
+--------------+----------------+-----------------+
|              | int32          | Integer         |
+--------------+----------------+-----------------+
|              | int64          | BigInteger      |
+--------------+----------------+-----------------+
| number       | *undefined*    | Float           |
+--------------+----------------+-----------------+
|              | float          | Float           |
+--------------+----------------+-----------------+
| string       | *undefined*    | String          |
+--------------+----------------+-----------------+
|              | password       | String          |
+--------------+----------------+-----------------+
|              | byte           | String          |
+--------------+----------------+-----------------+
|              | binary         | LargeBinary     |
+--------------+----------------+-----------------+
|              | date           | Date            |
+--------------+----------------+-----------------+
|              | date-time      | DateTime        |
+--------------+----------------+-----------------+
| boolean      |                | Boolean         |
+--------------+----------------+-----------------+

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
