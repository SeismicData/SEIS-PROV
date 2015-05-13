#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script generating Python code, PROV-XML examples, and plots from the JSON
definitions.

:copyright:
    Lion Krischer (lion.krischer@geophysik.uni-muenchen.de), 2015
:license:
    The MIT License (MIT)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import io
import json
import os
import uuid
import shutil

NS_PREFIX = "seis_prov"
NS_URL = "http://seisprov.org/seis_prov/0.0/#"


TEMPLATE = """
import prov.constants
import prov.model

NS_PREFIX = "{prefix}"
NS_SEIS = (NS_PREFIX, "{url}")

pr = prov.model.ProvDocument()
pr.add_namespace(*NS_SEIS)

pr.{type}("{prefix}:001_{two_letter_code}_{short_hash}", other_attributes=((
    ("prov:label", "{label}"),
    ("prov:type", "{prefix}:{name}"),
{contents}
))
""".strip()


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
definitions_dir = os.path.join(current_dir, "definitions")
schema_filename = os.path.abspath(
    os.path.join(definitions_dir, "schema.json"))


generated_dir = os.path.join(current_dir, "_generated")
python_dir = os.path.join(generated_dir, "python")
xml_dir = os.path.join(generated_dir, "xml")
plot_dir = os.path.join(generated_dir, "plots")

if os.path.exists(generated_dir):
    shutil.rmtree(generated_dir)

os.makedirs(python_dir)
os.makedirs(xml_dir)
os.makedirs(plot_dir)


def json_files(folder, exclude_filenames):
    """
    Generator yielding all JSON definition files as absolute paths.

    :param folder: Folder to recursively search into.
    :param exclude_filenames: List of absolute file paths to exclude.
    """
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[-1].lower() != ".json":
                continue
            filename = os.path.abspath(os.path.join(dirpath, filename))
            if filename in exclude_filenames:
                continue
            yield filename


def generate_python_code():
    for filename in json_files(definitions_dir,
                               exclude_filenames=[schema_filename]):
        with io.open(filename, "rt") as fh:
            definition = json.load(fh)
        # We will always generate two sets: a minimal one containing only the
        # bare minimum amount of information and a maximal one containing as
        # much as possible.
        py_min_filename = os.path.join(
            python_dir, "%s_%s_min.py" % (
                definition["type"],
                os.path.splitext(os.path.basename(filename))[0]))
        py_max_filename = os.path.join(
            python_dir, "%s_%s_max.py" % (
                definition["type"],
                os.path.splitext(os.path.basename(filename))[0]))

        # Create the minimum one.
        contents = []
        for attrib in definition["attributes"]:
            if not attrib["required"]:
                continue
            # For the example, only use the first type.
            d_type = attrib["types"][0]
            # Strings are simple.
            if d_type == "xsd:string":
                contents.append('("%s:%s", "%s")' % (
                    NS_PREFIX, attrib["name"], attrib["example_value"]))
            # Others harders as they have to be represented as literals.
            else:
                contents.append(
                    '("{prefix}:{name}", prov.model.Literal(\n'
                    '        {repr},\n        prov.constants.{type}))'.format(
                        prefix=NS_PREFIX,
                        name=attrib["name"],
                        repr=repr(attrib["example_value"]),
                        type=d_type.replace(":", "_").upper()))
        contents = ",\n    ".join(contents)
        if contents:
            contents = "    " + contents
        file_contents = TEMPLATE.format(
            prefix=NS_PREFIX,
            type=definition["type"],
            two_letter_code=definition["two_letter_code"],
            short_hash=str(uuid.uuid4()).replace("-", "")[:7],
            label=definition["recommended_label"],
            name=definition["name"],
            url=NS_URL,
            contents=contents)
        with open(py_min_filename, "wt") as fh:
            fh.write(file_contents)

        # Create the maximum one.
        contents = []
        for attrib in definition["attributes"]:
            if "skip_example_in_doc" in attrib and \
                    attrib["skip_example_in_doc"]:
                continue
            # For the example, only use the first type.
            d_type = attrib["types"][0]
            # Strings are simple.
            if d_type == "xsd:string":
                contents.append('("%s:%s", "%s")' % (
                    NS_PREFIX, attrib["name"], attrib["example_value"]))
            # Others harders as they have to be represented as literals.
            else:
                contents.append(
                    '("{prefix}:{name}", prov.model.Literal(\n'
                    '        {repr},\n        prov.constants.{type}))'.format(
                        prefix=NS_PREFIX,
                        name=attrib["name"],
                        repr=repr(attrib["example_value"]),
                        type=d_type.replace(":", "_").upper()))
        contents = ",\n    ".join(contents)
        if contents:
            contents = "    " + contents
        file_contents = TEMPLATE.format(
            prefix=NS_PREFIX,
            type=definition["type"],
            two_letter_code=definition["two_letter_code"],
            short_hash=str(uuid.uuid4()).replace("-", "")[:7],
            label=definition["recommended_label"],
            name=definition["name"],
            url=NS_URL,
            contents=contents)
        with open(py_max_filename, "wt") as fh:
            fh.write(file_contents)


if __name__ == "__main__":
    generate_python_code()
