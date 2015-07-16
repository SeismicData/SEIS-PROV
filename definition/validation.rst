Validation
==========

How to Validate a SEIS-PROV Document
------------------------------------

With a format as complex as ``SEIS-PROV``, validation, e.g. assuring any given
file is a valid ``SEIS-PROV`` file, is crucial. As ``SEIS-PROV`` is W3C PROV
with some additional constraints, this is a two step procedure:

1. Make sure the file is a valid W3C PROV document.
2. Assert that the additional constraints are followed.

Not all of the constraints can be enforced with a schema based validation so a
custom validator is necessary. The constraints for the various record types are
defined in a JSON file which acts as a schema for ``SEIS-PROV`` records. It can
be found here:

.. toctree::
    :maxdepth: 2
    :glob:

    schema


A reference implementation of such a validator is also part of the
``SEIS-PROV`` definition. In case you want to develop your own validator,
please read the definition. The reference validator has largely been developed
around two sets of test files: A large number of valid files and a number of
invalid files with comments denoting why they are not valid. You can use this
alongside the schema as a starting point.

* `Valid Files <https://github.com/SeismicData/SEIS-PROV/tree/master/validator/seis_prov_validate/test_data/valid_files>`_
* `Invalid Files <https://github.com/SeismicData/SEIS-PROV/tree/master/validator/seis_prov_validate/test_data/invalid_files>`_

Official Validator
------------------

Installation
^^^^^^^^^^^^

The validator is written in Python and currently supports Python 2.7, 3.3, and
3.4. Additionally it requires the following Python modules:

* ``jsonschema>=2.4.0``
* ``lxml``
* ``prov``
* ``pytest``
* ``six``

As it is  not yet released, you will have to install from GitHub:


.. code-block:: bash

     $ git clone https://github.com/SeismicData/SEIS-PROV.git
     $ cd SEIS-PROV/validator
     $ pip install -v -e .


You can test your installation with

.. code-block:: bash

    $ python -m seis_prov_validate.test_validator
    ................................................................
    ................................................................
    ...........................................................
    ================== 500 passed in 0.91 seconds ==================



Command Line Usage
^^^^^^^^^^^^^^^^^^

The module will install a single command: ``seis-prov-validate``.

.. code-block:: bash

    $ seis-prov-validate prov.xml
    VALID SEIS-PROV FILE!

Any other output mean your file is not valid. The error messages should
hopefully give hints on how to fix it.

Library Usage
^^^^^^^^^^^^^

Usage as a library is also possible. The module exports a single relevant
function: ``seis_prov_validate.validate()``

.. code-block:: python

    >>> from seis_prov_validate import validate
    >>> result = validate("./valid_files/waveform_trace_min.xml")
    >>> result.is_valid
    True
    >>> result.warnings
    []
    >>> result.errors
    []

    >>> result = validate("./invalid_files/waveform_with_extra_attribute.xml")
    >>> result.is_valid
    False
    >>> result.warnings
    []
    >>> result.errors
    ["Record 'seis_prov:sp001_wf_c17dd1f' has an additional attribute in "
     "the SEIS-PROV namespace: 'something'. This is not allowed for this record type."]



Actions the Validator Performs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following is a sequence of actions the official validator performs. A valid
``SEIS-PROV`` document must not fail any of these.

1. Check if its a JSON or an XML file.
2. Parse the document with the `Python prov package <prov.readthedocs.org>`_.
   It can currently read *PROV-JSON* and *PROV-XML* serialized documents.
3. Write the document as *PROV-XML* and validate against the *PROV-XML* XSD
   schema. This to a large parts assures the document is valid according to the
   W3C PROV specification.
4. Make sure it has a ``SEIS-PROV`` namespace. Otherwise it is a valid W3C PROV
   document but does not contain anything from ``SEIS-PROV``.
5. For the root document and each bundle in the document, find each provenance
   record and assert the following things.

   1. If the record has an id or a **prov:type** in the ``SEIS-PROV``
      namespace, it must be one of the four ``SEIS-PROV`` record types.
   2. If not, skip this record. It is not part of ``SEIS-PROV`` but still valid
      W3C PROV as we already validated against the W3C PROV schema.
   3. Make sure the record has exactly one **prov:type** attribute.
   4. Make sure the given ``SEIS-PROV`` type is valid and exists.
   5. Validate each ``SEIS-PROV`` id against the regular expression.
   6. Make sure the **prov:label** is correct.
   7. Validate the attributes against the definitions in the JSON schema.
