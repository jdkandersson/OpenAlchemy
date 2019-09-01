Type Mapping
============

*openapi-SQLAlchemy* translates *openapi* types to *SQLalchemy* types using
the following mapping:

+--------------+----------------+-----------------+
| openapi type | openapi format | SQLAlchemy type |
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
| string       |                | String          |
+--------------+----------------+-----------------+
| boolean      |                | Boolean         |
+--------------+----------------+-----------------+

string
------

*openapi* optionally allows the *maxLength* property for *strings*. This is
translated to the *length* argument for the *SQLAlchemy* *String*, which is set
to *None* if *maxLength* is *undefined*.
