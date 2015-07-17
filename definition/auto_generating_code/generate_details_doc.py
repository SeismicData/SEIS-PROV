#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
:copyright:
    Lion Krischer (lion.krischer@googlemail.com), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import json
import os
import sys

sys.path.append(".")

from header import (get_filename, current_dir, activity_dir, entity_dir,
                    agent_dir)  # NOQA

with io.open(os.path.join(current_dir, os.pardir,
                          "details.rst.template"), "rt") as fh:
    DETAILS_TEMPLATE = fh.read()

TEMPLATE = """
------

{title}
{title_line}

{description}

.. raw:: html

    <div id="tab-container" class="tab-container">
      <ul class='etabs'>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-description">Definition</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-json_def">JSON Definition</a>
        </li>
      </ul>
      <div class="tab-contents" id="tabs-{node_type}-{name}-description">


Properties
    ============================ =======
    Name                         Value
    ============================ =======
    ``prov:id``                  ``{name}``
    ``prov:label``               ``{label}``
    Two letter ID code:          ``{two_letter_code}``
    ============================ =======

Required Attributes
{required_attributes}

Optional Attributes
{optional_attributes}


.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-json_def">

This shows the JSON that is used to generate the rest of the definition.

.. literalinclude:: {json_def_file}
    :language: json

.. raw:: html

    </div>
    </div>
""".strip()


EXAMPLE_TEMPLATE = """
**{example_title}**

{description}

.. raw:: html

    <div id="tab-container" class="tab-container">
      <ul class='etabs'>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-{ex}-graph">Graph</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-{ex}-python">Python Code</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-{ex}-xml">PROV-XML</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-{ex}-json">PROV-JSON</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-{ex}-provn">PROV-N</a>
        </li>
      </ul>
      <div class="tab-contents" id="tabs-{node_type}-{name}-{ex}-graph">

.. graphviz:: {dotfile}

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-{ex}-python">

Python code utilizing the `prov <http://prov.readthedocs.org/>`_ package.

.. literalinclude:: {pythonfile}
    :language: python

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-{ex}-xml">

In the `PROV-XML <http://www.w3.org/TR/prov-xml/>`_ serialization.

.. literalinclude:: {xmlfile}
    :language: xml

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-{ex}-json">

In the
`PROV-JSON <http://www.w3.org/Submission/2013/SUBM-prov-json-20130424/>`_
serialization.

.. literalinclude:: {jsonfile}
    :language: json

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-{ex}-provn">

In `PROV-N <http://www.w3.org/TR/prov-n/>`_ notation.

.. literalinclude:: {provnfile}

.. raw:: html

    </div>
    </div>
""".strip()


def json_files(folder):
    """
    Generator yielding all JSON definition files as absolute paths.

    :param folder: Folder to recursively search into.
    """
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[-1].lower() != ".json":
                continue
            filename = os.path.abspath(os.path.join(dirpath, filename))
            yield filename


def create_details_rst():
    agents = []
    for filename in json_files(folder=agent_dir):
        agents.append(create_rst_representation(filename))
    agents = "\n\n\n".join(agents)

    entities = []
    for filename in json_files(folder=entity_dir):
        entities.append(create_rst_representation(filename))
    entities = "\n\n\n".join(entities)

    activities = []
    for filename in json_files(folder=activity_dir):
        activities.append(create_rst_representation(filename))
    activities = "\n\n\n".join(activities)

    with io.open(os.path.join(current_dir, os.pardir,
                              "_generated_details.rst"), "wt") as fh:
        fh.write(DETAILS_TEMPLATE.format(
            entities=entities,
            activities=activities,
            agents=agents))


def make_table(lines, prefix):
    """
    Helper function creating and RST table. The first line is interpreted as
    the header values.
    """
    if len(lines) == 1:
        return "%s*None*" % prefix

    # Get the max length of each item.
    lengths = [[len(_j) for _j in _i] for _i in lines]
    lengths = [max(_j[_i] for _j in lengths) for _i in range(len(lines[0]))]

    fmt = "  ".join("%-{0}s".format(_i) for _i in lengths)
    border = "  ".join("=" * _i for _i in lengths)

    lines = [fmt % _i for _i in lines]
    lines.insert(0, border)
    lines.insert(2, border)
    lines.append(border)

    return prefix + ("\n%s" % prefix).join(lines)


def create_rst_representation(json_file):
    with io.open(json_file, "rt") as fh:
        data = json.load(fh)
    node_type = os.path.basename(os.path.dirname(json_file))
    # Do the attributes first.
    required_attributes = [("Name", "Type", "Description")]
    optional_attributes = [("Name", "Type", "Description")]

    for attrib in data["attributes"]:
        obj = required_attributes if attrib["required"] \
            else optional_attributes
        obj.append((
            attrib["name"],
            ", ".join("``%s``" % _i for _i in attrib["types"]),
            attrib["description"]))

    if data["name"] == "person":
        title = "Person"
    elif data["name"] == "software_agent":
        title = "Software Agent"
    elif data["name"] == "organization":
        title = "Organization"
    else:
        title = "%s" % (data["label"])

    text = TEMPLATE.format(
        title=title,
        title_line="^" * len(title),
        description=data["description"],
        two_letter_code=data["two_letter_code"],
        label=data["label"],
        required_attributes=make_table(required_attributes, prefix="    "),
        optional_attributes=make_table(optional_attributes, prefix="    "),
        json_def_file=os.path.relpath(json_file),
        name=data["name"],
        node_type=node_type)

    if len(optional_attributes) > 1:
        example = EXAMPLE_TEMPLATE.format(
            example_title="Minimal Example",
            description="A concrete ``%s`` node example is illustrated "
            "here as a graph, in code, and in various representations. This "
            "is a minimal but valid ``%s`` node. See below for a full "
            "example." % (data["name"], data["name"]),
            name=data["name"],
            dotfile=os.path.relpath(get_filename(
                json_file, node_type, "dot", "min")),
            pythonfile=os.path.relpath(get_filename(
                json_file, node_type, "py", "min")),
            xmlfile=os.path.relpath(get_filename(
                json_file, node_type, "xml", "min")),
            jsonfile=os.path.relpath(get_filename(
                json_file, node_type, "json", "min")),
            provnfile=os.path.relpath(get_filename(
                json_file, node_type, "provn", "min")),
            node_type=node_type,
            ex="ex_min")

        example += "\n\n\n" + EXAMPLE_TEMPLATE.format(
            example_title="Full Example",
            description="A concrete ``%s`` node example is illustrated "
            "here as a graph, in code, and in various representations. This "
            "is a full ``%s`` node containing the maximum amount of "
            "information." % (data["name"], data["name"]),
            name=data["name"],
            dotfile=os.path.relpath(get_filename(
                json_file, node_type, "dot", "max")),
            pythonfile=os.path.relpath(get_filename(
                json_file, node_type, "py", "max")),
            xmlfile=os.path.relpath(get_filename(
                json_file, node_type, "xml", "max")),
            jsonfile=os.path.relpath(get_filename(
                json_file, node_type, "json", "max")),
            provnfile=os.path.relpath(get_filename(
                json_file, node_type, "provn", "max")),
            node_type=node_type,
            ex="ex_max")

    else:
        example = EXAMPLE_TEMPLATE.format(
            example_title="Example",
            description="A concrete ``%s`` node example is illustrated "
            "here as a graph, in code, and in various representations." %
            data["name"],
            name=data["name"],
            dotfile=os.path.relpath(get_filename(
                json_file, node_type, "dot", "max")),
            pythonfile=os.path.relpath(get_filename(
                json_file, node_type, "py", "max")),
            xmlfile=os.path.relpath(get_filename(
                json_file, node_type, "xml", "max")),
            jsonfile=os.path.relpath(get_filename(
                json_file, node_type, "json", "max")),
            provnfile=os.path.relpath(get_filename(
                json_file, node_type, "provn", "max")),
            node_type=node_type,
            ex="ex")

    return text + "\n\n\n" + example


if __name__ == "__main__":
    create_details_rst()
