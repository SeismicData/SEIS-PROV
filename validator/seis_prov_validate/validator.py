#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validator for SEIS-PROV files.

:copyright:
    Lion Krischer (lion.krischer@googlemail.com), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import inspect
import io
import json
import os
import re
import six
from six.moves.urllib.parse import urlparse
import warnings
import sys

import jsonschema
from lxml import etree
import prov
import prov.constants
import prov.identifier

# Directory of the file.
_DIR = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))

_PROV_XML_SCHEMA = os.path.join(_DIR, "schemas", "prov.xsd")
_SEIS_PROV_SCHEMA = os.path.join(_DIR, "schemas", "seis_prov.json")

SEIS_PROV_NAMESPACE = "http://seisprov.org/seis_prov/0.1/#"

# Caches to speed up repeated runs.
__JSON_SCHEMA_CACHE = []
__XSD_SCHEMA_CACHE = []

_PERSON = prov.identifier.QualifiedName(prov.constants.PROV, "Person")
_SOFTWARE_AGENT = prov.identifier.QualifiedName(prov.constants.PROV,
                                                "SoftwareAgent")
_ORGANIZATION = prov.identifier.QualifiedName(prov.constants.PROV,
                                              "Organization")


def _check_json_schema():
    """
    Validate the JSON schema itself to avoid silly errors. Only done once to
    speedup successive calls.
    """
    if not __JSON_SCHEMA_CACHE:
        with io.open(_SEIS_PROV_SCHEMA, "rt") as fh:
            schema = json.load(fh)

        # Make sure the namespace in the scheme checks out to be identical
        # to the one used here.
        if schema["_metainformation"]["namespace"] != SEIS_PROV_NAMESPACE:
            raise ValueError("Internal problem. The SEIS-PROV namespace in "
                             "the schema is not equal to the expected one.")

        jsonschema.Draft4Validator.check_schema(schema)
        __JSON_SCHEMA_CACHE.append(schema)

    return __JSON_SCHEMA_CACHE[0]


def _is_xml_file(file_object):
    """
    Helper function testing if a file is an XML file.

    :param file_object: Open file or file-like object to test.
    """
    try:
        etree.parse(file_object)
        return True
    except:
        return False


def _is_json_file(file_object):
    """
    Helper function testing if a file is valid JSON file.

    :param file_object: Open file or file-like object to test.
    """
    # Has to be decoded to a string to work with json.
    with io.StringIO(file_object.read().decode()) as fh:
        try:
            json.load(fh)
            return True
        except:
            return False


class SeisProvValidationException(Exception):
    def __init__(self, message):
        self.message = message


class SeisProvValidationWarning(UserWarning):
    pass


def _log_error(message):
    """
    Print the message to stdout and exit with a non-zero exit code.
    """
    raise SeisProvValidationException(message)


def _log_warning(message):
    """
    Print the message to stdout
    """
    warnings.warn(message, SeisProvValidationWarning)


class SeisProvValidationResult(object):
    def __init__(self, errors, warnings):
        self.errors = errors
        self.warnings = warnings

    @property
    def is_valid(self):
        return not bool(self.errors)

    def __str__(self):
        ret_str = ""
        for error in self.errors:
            ret_str += "%s\n" % error
        for warning in self.warnings:
            ret_str += "WARNING: %s\n" % warning
        if self.is_valid:
            ret_str += "VALID SEIS-PROV FILE!"
        return ret_str.strip()


def validate(file_or_object):
    """
    Validate a given SEIS-PROV file.

    :param file_or_object: The filename or file-like object to validate.
    """
    errors = []
    warns = []

    with warnings.catch_warnings(record=True) as w:
        warnings.resetwarnings()
        warnings.simplefilter("always")

        try:
            _validate(file_or_object)
        except SeisProvValidationException as e:
            errors.append(e.message)

    for warn in w:
        warn = warn.message
        if not isinstance(warn, SeisProvValidationWarning):
            continue
        warns.append(warn.args[0])

    return SeisProvValidationResult(errors=errors,
                                    warnings=warns)


def _validate(file_or_object):
    """
    Validate a given SEIS-PROV file.

    This function is a helper routine and either opens the file if necessary or
    just passes the file pointer.

    :param file_or_object: The filename or file-like object to validate.
    """
    if isinstance(file_or_object, six.string_types):
        # Check if the file exists.
        if not os.path.exists(file_or_object):
            _log_error("Path '%s' does not exist." % file_or_object)
        # Make sure its a file.
        if not os.path.isfile(file_or_object):
            _log_error("Path '%s' is not a file." % file_or_object)
        with io.open(file_or_object, "rb") as fh:
            return __validate_seis_prov(fh)
    else:
        return __validate_seis_prov(file_or_object)


def __validate_seis_prov(file_object):
    """
    Core validation function.

    :param file_object: Open file or file-like object.
    """
    original_position = file_object.tell()
    # Step 1: Check and read the JSON schema.
    json_schema = _check_json_schema()

    # Determine file type.
    is_json = _is_json_file(file_object)
    file_object.seek(original_position, 0)
    is_xml = _is_xml_file(file_object)
    file_object.seek(original_position, 0)

    if is_json is False and is_xml is False:
        _log_error("File is neither a valid JSON nor a valid XML file.")
    elif is_json is True and is_xml is True:
        # Should not happen for obvious reasons...
        raise NotImplementedError
    elif is_json:
        fileformat = "json"
    elif is_xml:
        fileformat = "xml"

    # Step 2: Attempt to read the provenance file with the prov Python package.
    try:
        doc = prov.read(file_object, format=fileformat)
    except Exception as e:
        _log_error("Could not parse the file with the prov Python library due"
                   " to: the following PROV error message: %s" % (repr(e)))

    # Step 3: Validate against the PROV XML XSD Scheme.
    _validate_against_xsd_scheme(doc)

    # Check if it has any records.
    if not doc._records:
        _log_error("File does not contain a single provenance record.")

    # Find the seis prov namespace. If it does not exist, it is still a
    # valid PROV document!
    for ns in doc.namespaces:
        if ns.uri == SEIS_PROV_NAMESPACE:
            break
    else:
        _log_warning("The document is a valid W3C PROV document but not a "
                     "single SEIS-PROV record has been found.")
        return

    # Step 4: Custom validation against the JSON schema. Validate the root
    # document as well as any bundles.
    seis_prov_ids = _validate_prov_bundle(doc, json_schema, ns=ns)
    for bundle in doc.bundles:
        seis_prov_ids.extend(
            _validate_prov_bundle(bundle, json_schema, ns=ns))

    if not seis_prov_ids:
        _log_warning("The document is a valid W3C PROV document but not a "
                     "single SEIS-PROV record has been found.")
        return

    # Find duplicate ids.
    duplicates = set([i for i in seis_prov_ids
                      if sum([1 for a in seis_prov_ids if a == i]) > 1])
    if duplicates:
        _log_error("One or more ids have been used more than once: %s" %
                   ", ".join(["'%s'" % _i for _i in duplicates]))


def _validate_prov_bundle(doc, json_schema, ns):
    """
    Custom validator for SEIS-PROV.
    """
    id_collector = []

    json_schema_map = {
        prov.model.PROV_ENTITY: json_schema["entities"],
        prov.model.PROV_ACTIVITY: json_schema["activities"],
        prov.model.PROV_AGENT: json_schema["agents"]}

    for record in doc._records:
        # I don't fully understand what the prov API intends to do with two
        # sets of attributes so we just create a union of them here.
        attrs = list(set(record.attributes).union(record.extra_attributes))

        if record.identifier:
            id_in_seis_prov_ns = record.identifier.namespace == ns
        else:
            id_in_seis_prov_ns = False

        # Find the prov type
        prov_type = [i[1] for i in attrs if i[0] == prov.model.PROV_TYPE]

        # Check if any of the prov:type's is in the SEIS-PROV namespace.
        prov_type_in_ns = False
        for t in prov_type:
            # If neither the prov type nor the id are in the SEIS-PROV
            # namespace it is not part of SEIS-PROV and so we don't validate
            # it.
            if isinstance(t, six.string_types):
                if t.startswith("%s:" % ns.prefix):
                    prov_type_in_ns = True
                    break
            elif isinstance(t, prov.model.Literal):
                if t.value.startswith("%s:" % ns.prefix):
                    prov_type_in_ns = True
                    break
            else:
                if t.namespace == ns:
                    prov_type_in_ns = True
                    break

        # Neither id not prov type in SEIS-PROV namespace. We don't have to
        # worry anymore.
        if not id_in_seis_prov_ns and not prov_type_in_ns:
            continue

        if len(prov_type) > 1:
            # As soon as either the id or any type is in the SEIS_PROV
            # namespace, this is no longer allowed.
            _log_error("Record '%s' has %i prov:type's set. Only one is "
                       "allowed as soon as any prov:type or the record's id "
                       "is in the SEIS-PROV namespace." %
                       (str(record.identifier), len(prov_type)))
        if not prov_type:
            # If the id is in the SEIS-PROV namespace, it must have a
            # prov_type.
            if id_in_seis_prov_ns:
                _log_error("Record '%s' has an id in the SEIS-PROV namespace "
                           "but no prov:type attribute. This is not allowed."
                           % str(record.identifier))
            continue
        prov_type = prov_type[0]

        rec_type = record.get_type()
        if rec_type not in (
                prov.model.PROV_ENTITY, prov.model.PROV_ACTIVITY,
                prov.model.PROV_AGENT) and record.identifier is None:
            continue

        # Now we need to deal with a couple of different failure cases.
        if prov_type_in_ns:
            # 1. It's prov_type is in the seis_prov namespace but the id is
            #    not. This is not valid.
            if not id_in_seis_prov_ns:
                _log_error("Record '%s' has a prov:type attribute in the "
                           "SEIS-PROV namespace but its id is not part of the "
                           "namespace. This is not allowed." %
                           (str(record.identifier)))
        else:
            # 2. If the prov type is not in the SEIS-PROV namespace but the id
            #    is, then it must either be a software agent or a person.
            #    Anything else is not allowed.
            if id_in_seis_prov_ns:
                if prov_type not in (_PERSON, _SOFTWARE_AGENT, _ORGANIZATION):
                    _log_error(
                        "Record '%s' has an id in the SEIS-PROV namespace "
                        "but its prov:type is neither in the SEIS-PROV "
                        "namespace nor is it a person, an organization, or a "
                        "software agent. This is not allowed." %
                        str(record.identifier))
            else:
                # This should not be able to happen as we check for this
                # combination a bit further up the code.
                raise NotImplementedError

        if prov_type == _PERSON:
            prov_type = "person"
        elif prov_type == _SOFTWARE_AGENT:
            prov_type = "software_agent"
        elif prov_type == _ORGANIZATION:
            prov_type = "organization"
        else:
            prov_type = assert_ns_and_extract(prov_type, ns)

        if rec_type not in json_schema_map:
            _log_error("%s not a record type that is valid for SEIS-PROV." %
                       str(rec_type))
        json_def = json_schema_map[rec_type]

        if prov_type not in json_def:
            _log_error("prov:type '%s' of record type '%s' is not known to "
                       "SEIS-PROV." % (prov_type, str(rec_type)))

        definition = json_def[prov_type]

        # If the id is in the SEIS-PROV namespace, it must adhere to the
        # regular expression of the documentation.
        if id_in_seis_prov_ns:
            id_regex = r"^sp\d{3,5}_" + definition["two_letter_code"] + \
                r"_[a-z0-9]{7,12}$"
            if re.match(id_regex, record.identifier.localpart) is None:
                _log_error("The local part of the identifier '%s' does not "
                           "match the regular expression '%s' as is required "
                           "by the standard."
                           % (str(record.identifier), id_regex))

        id_collector.append(record.identifier.localpart)

        # Validate the label.
        prov_label = [i for i in attrs if i[0] == prov.model.PROV_LABEL]
        if not prov_label:
            _log_error("Record '%s' does not have a prov:label set." %
                       str(record.identifier))
        elif len(prov_label) > 1:
            _log_error("Record '%s' has %i prov:label's set. Only one is "
                       "allowed." % (str(record.identifier), len(prov_label)))
        prov_label = prov_label[0][1]

        # '*' is a special label for agents.
        if definition["label"] != "*" and definition["label"] != prov_label:
            _log_error("Record '%s' has label '%s' instead of '%s'." % (
                       str(record.identifier), prov_label,
                       definition["label"]))

        # Get all attributes which are part of the seis prov namespace. All
        # others don't matter for the sake of validation.
        attrs = [_i for _i in attrs
                 if isinstance(_i[0], prov.model.QualifiedName) and
                 _i[0].namespace == ns]

        # Make sure it has all required attributes.
        required_attributes = set([_i["name"]
                                   for _i in definition["attributes"]
                                   if _i["required"]])
        available_attributes = set([_i[0].localpart for _i in attrs])
        missing_attributes = sorted(required_attributes.difference(
            available_attributes))

        if missing_attributes:
            _log_error("Record '%s' misses the following required "
                       "attributes in the SEIS-PROV namespace: %s" %
                       (str(record.identifier),
                        ", ".join("'%s'" % _i for _i in missing_attributes)))

        # Validate each attribute.
        for attr in attrs:
            name, value = attr[0].localpart, attr[1]
            this_def = [i for i in definition["attributes"]
                        if i["name"] == name]

            if not this_def and \
                    not definition["other_seis_prov_attributes_allowed"]:
                _log_error("Record '%s' has an additional attribute in the "
                           "SEIS-PROV namespace: '%s'. This is not allowed "
                           "for this record type." % (str(record.identifier),
                                                      name))
            elif not this_def:
                # In some instances its allowed.
                continue

            this_def = this_def[0]
            _validate_type(name, value, this_def["types"])

            # Also validate the patterns if any.
            if "pattern" in this_def:
                if "xsd:string" not in this_def["types"]:
                    # This should not happen.
                    raise Exception
                if re.match(this_def["pattern"], value) is None:
                    _log_error("Attribute '%s' in record '%s' with the value "
                               "'%s' does not match the regex '%s'." % (
                                name, str(record.identifier), value,
                                this_def["pattern"]))
    return id_collector


# Collection of functions performing the actual type validation. Should return
# True/False. If an error occurs it will be considered to not be of that type.
TYPE_MAP = {
    "xsd:double": lambda x: isinstance(x, float),
    "xsd:decimal": lambda x: float(x.value) is not None,
    "xsd:integer": lambda x: str(x).isnumeric(),
    "xsd:positiveInteger": lambda x:
        (isinstance(x, int) and int(x) >= 0) or
        (x.value.isnumeric() and int(x.value) >= 0),
    "xsd:string": lambda x: isinstance(x, six.string_types) and bool(x),
    "xsd:dateTime": lambda x: isinstance(x, datetime.datetime),
    "xsd:anyURI": lambda x: (isinstance(x, six.string_types) and
                             bool(urlparse(x))) or bool(urlparse(x.uri))
}


def _validate_type(value_name, value, possible_types):
    """
    Validate the possible types and also check the values if possible.
    """
    for t in possible_types:
        if t not in TYPE_MAP:
            raise NotImplementedError
        try:
            if TYPE_MAP[t](value) is True:
                break
        except:
            continue
    else:
        _log_error("Attribute '%s' has an invalid type '%s'. Valid types: %s"
                   % (value_name, type(value), ", ".join(possible_types)))


def assert_ns_and_extract(name, ns):
    """
    Makes sure the given name is under the given namespace and extract the
    name.
    """
    prefix = "%s:" % ns.prefix
    if not name.startswith(prefix):
        _log_error("Record %s does not start with %s" % (name, prefix))
    return name[len(prefix):]


def _validate_against_xsd_scheme(doc):
    # Serialize to XML (this makes it work with JSON and others as well).
    buf = io.BytesIO()
    doc.serialize(destination=buf, format="xml")
    buf.seek(0, 0)

    xml_doc = etree.parse(buf)
    if not __XSD_SCHEMA_CACHE:
        __XSD_SCHEMA_CACHE.append(
            etree.XMLSchema(etree.parse(_PROV_XML_SCHEMA)))

    xml_schema = __XSD_SCHEMA_CACHE[0]

    is_valid = xml_schema.validate(xml_doc)
    if is_valid:
        return

    _log_error("SEIS-PROV document did not pass validation against the "
               "PROV-XML schema:\n\t%s" % "\n\t".join(
                   str(i) for i in xml_schema.error_log))


def main():
    parser = argparse.ArgumentParser(
        description="Validator for SEIS-PROV files.")
    parser.add_argument("filename", help="Filename of the SEIS-PROV file.")
    args = parser.parse_args()

    filename = args.filename

    result = validate(filename)
    print(result)
    if not result.is_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()
