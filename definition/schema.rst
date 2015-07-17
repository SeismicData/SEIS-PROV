Schema
------

:download:`Download <_generated/seis_prov.json>`

A JSON file inspired by JSON schema is used to describe the various agents,
entities, and activities in ``SEIS-PROV``. If a ``SEIS-PROV`` record is
discovered it has to be validated against the scheme for that particular
record. The JSON "schema" furthermore determines which types are valid
``SEIS-PROV`` types. It is a vital component of any program validating
``SEIS-PROV`` files.

Structure
=========

At the top-level the file has a ``_metainformation`` key that determines the
namespace and version of ``SEIS-PROV``.

.. code-block:: python

    "_metainformation": {
        "format": "SEIS-PROV",
        "namespace": "http://seisprov.org/seis_prov/0.1/#",
        "recommended_namespace_prefix": "seis_prov",
        "version": "0.1"
    }

Entities, agents, and activities are defined under the ``entities``,
``agents``, and ``activities`` keys. Each record is described by a JSON
object adhering to this schema.

:download:`Download Record JSON Schema <definitions/record_schema.json>`

We will illustrate this on the example of the multiplication activity as it
is a very basic example. Keep in mind that the documentation is also build
from this definition so everything will always be consistent.

.. literalinclude:: definitions/activities/multiply.json
    :language: json

Each record definition has the following keys:

``package``
    Which package this belongs to. Will always be ``seis_prov``.

``type``
    The type of record. One of ``activity``, ``entity``, ``agent``.

``name``
    The name of that particular record.

``two_letter_code``
    Used in the id of each record.

``label``
    Pretty version of the name. Will be the **prov:label** of each record.

``description``
    An arbitrarily long description of the record which can contain
    restructured text.

``other_seis_prov_attributes_allowed``
    Boolean indicating if the record can have attributes under the
    ``SEIS-PROV`` record aside from the ones defined for it.

``attributes``
    A list of required and optional attributes for that record.


Attributes
^^^^^^^^^^

Each attribute is again a JSON object, this time with the following keys:

``name``
    The name of that record.

``types``
    A list of allowed types as strings. The types are
    `XML Schema types <http://www.w3.org/TR/xmlschema-2/>`_.

``description``
    A description of that attribute.

``required``
    A flag denoting if the attribute is required or not.

``example_value``
    An example value for the attribute. This is only used to generate the
    documentation.

``pattern``
    This is optional. If given the value of that attribute must match the
    given regular expression.

