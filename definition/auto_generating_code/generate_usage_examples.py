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
                          "usage_examples.rst.template"), "rt") as fh:
    GENERATED_USAGE_EXAMPLES_TEMPLATE = fh.read()

# Examples to include
EXAMPLES = ["example_detailed_processing_chain",
            "example_schematic_processing_chain",
            "example_waveform_simulation",
            "example_cross_correlation"]


TEMPLATE = """
.. raw:: html

    <div id="tab-container" class="tab-container">
      <ul class='etabs'>
        <li class='tab'>
            <a href="#tabs-{filename}-graph">Graph</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{filename}-python">Python Code</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{filename}-xml">PROV-XML</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{filename}-json">PROV-JSON</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{filename}-provn">PROV-N</a>
        </li>
      </ul>
      <div class="tab-contents" id="tabs-{filename}-graph">

.. graphviz:: _generated/dot/examples/{filename}.dot

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{filename}-python">

Python code utilizing the `prov <http://prov.readthedocs.org/>`_ package.

.. literalinclude:: _generated/python/examples/{filename}.py
    :language: python

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{filename}-xml">

In the `PROV-XML <http://www.w3.org/TR/prov-xml/>`_ serialization.

.. literalinclude:: _generated/xml/examples/{filename}.xml
    :language: xml

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{filename}-json">

In the
`PROV-JSON <http://www.w3.org/Submission/2013/SUBM-prov-json-20130424/>`_
serialization.

.. literalinclude:: _generated/json/examples/{filename}.json
    :language: json

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{filename}-provn">

In `PROV-N <http://www.w3.org/TR/prov-n/>`_ notation.

.. literalinclude:: _generated/provn/examples/{filename}.provn

.. raw:: html

    </div>
    </div>
""".strip()


def create_generated_details_rst():
    kwargs = {}
    for example in EXAMPLES:
        kwargs[example] = TEMPLATE.format(filename=example)

    with io.open(os.path.join(current_dir, os.pardir,
                              "_generated_usage_examples.rst"), "wt") as fh:
        fh.write(GENERATED_USAGE_EXAMPLES_TEMPLATE.format(**kwargs))


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
    create_generated_details_rst()
