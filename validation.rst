Validation
==========

How to validate if something is a valid ``SEIS-PROV`` record.


Actions the Validator Performs
------------------------------

The following is a sequence of actions the official validator performs. A valid
``SEIS-PROV`` document must not fail any of these.

1. Parse the document with the `Python prov package <prov.readthedocs.org>`_.
   It can currently read *PROV-JSON* and *PROV-XML* serialized documents.
2. Write the document as *PROV-XML* and validate against the *PROV-XML* XSD
   schema. This to a large parts assures the document is valid according to the
   W3C PROV specification.
3. Make sure it has a ``SEIS-PROV`` namespace. Otherwise it is a valid W3C PROV
   document but does not contain anything from ``SEIS-PROV``.
4. For the root document and each bundle in the document
