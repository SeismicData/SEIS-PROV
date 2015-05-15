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

import glob
import io
import json
import os
import uuid
import sys

sys.path.append(".")

from header import (NS_PREFIX, NS_URL, definitions_dir, json_files,
                    get_filename, examples_dir) # NOQA

BASIC_HEADER = """
import prov.constants
import prov.model

NS_PREFIX = "{prefix}"
NS_SEIS = (NS_PREFIX, "{url}")

pr = prov.model.ProvDocument()
pr.add_namespace(*NS_SEIS)
""".strip().format(
    prefix=NS_PREFIX,
    url=NS_URL)


TEMPLATE = (BASIC_HEADER + """\n\n
pr.{type}("{prefix}:001_{two_letter_code}_{short_hash}", other_attributes=((
    ("prov:label", "{label}"),
    ("prov:type", "{prefix}:{name}"),
{contents}
)))
""").strip()


def generate_code():
    for filename in json_files(definitions_dir):
        with io.open(filename, "rt") as fh:
            definition = json.load(fh)

        node_type = os.path.basename(os.path.dirname(filename))

        # We will always generate two sets: a minimal one containing only the
        # bare minimum amount of information and a maximal one containing as
        # much as possible.
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
        min_file_contents = TEMPLATE.format(
            prefix=NS_PREFIX,
            type=definition["type"],
            two_letter_code=definition["two_letter_code"],
            short_hash=str(uuid.uuid4()).replace("-", "")[:7],
            label=definition["recommended_label"],
            name=definition["name"],
            contents=contents)
        with open(get_filename(filename, node_type, "py", "min"), "wt") as fh:
            fh.write(min_file_contents)

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
        max_file_contents = TEMPLATE.format(
            prefix=NS_PREFIX,
            type=definition["type"],
            two_letter_code=definition["two_letter_code"],
            short_hash=str(uuid.uuid4()).replace("-", "")[:7],
            label=definition["recommended_label"],
            name=definition["name"],
            url=NS_URL,
            contents=contents)
        with open(get_filename(filename, node_type, "py", "max"), "wt") as fh:
            fh.write(max_file_contents)

        # Create dot files with some more code generation.
        exec(
            min_file_contents +
            "\n\nfrom prov import dot\n"
            "dot.prov_to_dot(pr, use_labels=True).write_dot('%s')\n" %
            get_filename(filename, node_type, "dot", "min"))
        exec(
            max_file_contents +
            "\n\nfrom prov import dot\n"
            "dot.prov_to_dot(pr, use_labels=True).write_dot('%s')\n" %
            get_filename(filename, node_type, "dot", "max"))

        # Same with the XML files.
        exec(min_file_contents + "\n\n"
             "pr.serialize('%s', format='xml')" %
             get_filename(filename, node_type, "xml", "min"))
        exec(max_file_contents + "\n\n"
             "pr.serialize('%s', format='xml')" %
             get_filename(filename, node_type, "xml", "max"))

        # And once again with JSON.
        jsonfile = get_filename(filename, node_type, "json", "min")
        exec(min_file_contents + "\n\n"
             "pr.serialize('%s', format='json')" % jsonfile)
        # Read again and write in a pretty fashion.
        with io.open(jsonfile, "rt") as fh:
            data = json.load(fh)
        with io.open(jsonfile, "wt") as fh:
            json.dump(data, fh, indent=4, separators=(',', ': '))

        jsonfile = get_filename(filename, node_type, "json", "max")
        exec(max_file_contents + "\n\n"
             "pr.serialize('%s', format='json')" % jsonfile)
        # Read again and write in a pretty fashion.
        with io.open(jsonfile, "rt") as fh:
            data = json.load(fh)
        with io.open(jsonfile, "wt") as fh:
            json.dump(data, fh, indent=4, separators=(',', ': '))


def generate_code_from_examples():
    for filename in glob.glob(os.path.join(examples_dir, "*.py")):
        with io.open(filename, "rt") as fh:
            code_str = BASIC_HEADER + "\n\n\n" + fh.read()

        # Write Python file.
        with open(get_filename(filename, "examples", "py"), "wt") as fh:
            fh.write(code_str)

        if "datetime(" in code_str:
            code_str = "from datetime import datetime\n" + code_str

        # Write dot file.
        exec(
            code_str +
            "\n\nfrom prov import dot\n"
            "dot.prov_to_dot(pr, use_labels=True).write_dot('%s')\n" %
            get_filename(filename, "examples", "dot"))

        # Write XML.
        exec(code_str + "\n\n"
             "pr.serialize('%s', format='xml')" %
             get_filename(filename, "examples", "xml"))

        # Write JSON.
        exec(code_str + "\n\n"
             "pr.serialize('%s', format='json')" %
             get_filename(filename, "examples", "json"))


if __name__ == "__main__":
    generate_code()
    generate_code_from_examples()
