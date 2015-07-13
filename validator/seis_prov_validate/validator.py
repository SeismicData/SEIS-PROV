#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validator for the SEIS-PROV files.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import inspect
import io
import json
import os
import sys

import jsonschema
from lxml import etree
import prov

# Directory of the file.
_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))

_PROV_XML_SCHEMA = os.path.join(_DIR, "schemas", "prov.xsd")
_SEIS_PROV_SCHEMA = os.path.join(_DIR, "schemas", "seis_prov.json")

SEIS_PROV_NAMESPACE = "http://seisprov.org/seis_prov/0.1/#"


def _log_error(message):
    """
    Print the message to stdout and exit with a non-zero exit code.
    """
    sys.exit(message)


def _log_warning(message):
    """
    Print the message to stdout
    """
    print(message)


def validate(filename):
    # Start with the very basic checks. Check if the file exists.
    if not os.path.exists(filename):
        _log_error("Path '%s' does not exist." % filename)
    # Make sure its a file.
    if not os.path.isfile(filename):
        _log_error("Path '%s' is not a file." % filename)

    # Step 1: Check the JSON schema.
    json_schema = _check_json_schema()

    # Step 2: Attempt to read the provenance file with the prov Python package.
    try:
        doc = prov.read(filename)
    except Exception as e:
        _log_error("Could not parse the file with the prov Python library due"
                   " to: the following PROV error message: %s" % (str(e)))

    # Step 3: Validate against the PROV XML XSD Scheme.
    _validate_against_xsd_scheme(doc)

    # Find the seis prov namespace.
    for ns in doc.namespaces:
        if ns.uri == SEIS_PROV_NAMESPACE:
            break
    else:
        _log_error("SEIS-PROV namespace not found in document!")

    # Step 4: Custom validation against the JSON schema. Validate the root
    # document as well as any bundles.
    _validate_prov_bundle(doc, json_schema, ns=ns)
    for bundle in doc.bundles:
        _validate_prov_bundle(bundle, json_schema, ns=ns)


def _validate_prov_bundle(doc, json_schema, ns):
    """
    Custom validator for SEIS-PROV.
    """
    json_schema_map = {
        prov.model.PROV_ENTITY: json_schema["entities"],
        prov.model.PROV_ACTIVITY: json_schema["activities"]}

    for record in doc._records:
        # Now we only care about records in the SEIS-PROV namespace.
        if record.identifier.namespace != ns:
            continue

        # XXX: I honestly don't quite understand this part of the prov API. For
        # now I assume attributes and additional attributes are identical.
        assert record.extra_attributes == record.attributes

        rec_type = record.get_type()

        if rec_type not in json_schema_map:
            _log_error("%s not a record type that is valid for SEIS-PROV." %
                       str(rec_type))

        ################
        # DEBUGGING START
        import sys
        __o_std__ = sys.stdout
        sys.stdout = sys.__stdout__
        from IPython.core.debugger import Tracer
        Tracer(colors="Linux")()
        sys.stdout = __o_std__
        # DEBUGGING END
        ################


def _validate_against_xsd_scheme(doc):
    # Serialize to XML (this makes it work with JSON and others as well).
    buf = io.BytesIO()
    doc.serialize(destination=buf, format="xml")
    buf.seek(0, 0)

    xml_doc = etree.parse(buf)
    xml_schema = etree.XMLSchema(etree.parse(_PROV_XML_SCHEMA))

    is_valid = xml_schema.validate(xml_doc)
    if is_valid:
        return

    _log_error("SEIS-PROV document did not pass validation against the "
               "PROV-XML schema:\n\t%s" % "\n\t".join(
                   str(i) for i in xml_schema.error_log))


def _check_json_schema():
    """
    Validate the JSON schema itself to avoid silly errors.
    """
    with io.open(_SEIS_PROV_SCHEMA, "rt") as fh:
        schema = json.load(fh)

    jsonschema.Draft4Validator.check_schema(schema)

    return schema


def main():
    parser = argparse.ArgumentParser(
        description="Validator for SEIS-PROV files.")
    parser.add_argument("filename", help="Filename of the SEIS-PROV file.")
    args = parser.parse_args()

    filename = args.filename

    validate(filename)

    print("Valid SEIS-PROV File!")


if __name__ == "__main__":
    main()
