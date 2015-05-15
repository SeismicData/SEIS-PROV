from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import json
import os
import sys

sys.path.append(".")

from header import (NS_PREFIX, NS_URL, get_filename,
                    current_dir, activity_dir, entity_dir)  # NOQA

with io.open(os.path.join(current_dir, "details.rst.template"), "rt") as fh:
    DETAILS_TEMPLATE = fh.read()

TEMPLATE = """
{title}
{title_line}

{description}

============================ =======
Two letter ID code:          ``{two_letter_code}``
Recommended ``prov:label``   ``{label}``
============================ =======

**Attributes**

{attributes}

**Example**

.. raw:: html

    <div id="tab-container" class="tab-container">
      <ul class='etabs'>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-graph">Graph</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-python">Python Code</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-xml">PROV-XML</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-json">PROV-JSON</a>
        </li>
        <li class='tab'>
            <a href="#tabs-{node_type}-{name}-provn">PROV-N</a>
        </li>
      </ul>
      <div class="tab-contents" id="tabs-{node_type}-{name}-graph">

.. graphviz:: {dotfile}

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-python">

Python code utilizing the `prov <http://prov.readthedocs.org/>`_ package.

.. literalinclude:: {pythonfile}
    :language: python

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-xml">

In the `PROV-XML <http://www.w3.org/TR/prov-xml/>`_ serialization.

.. literalinclude:: {xmlfile}
    :language: xml

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-json">

In the
`PROV-JSON <http://www.w3.org/Submission/2013/SUBM-prov-json-20130424/>`_
serialization.

.. literalinclude:: {jsonfile}
    :language: json

.. raw:: html

    </div>
    <div class="tab-contents" id="tabs-{node_type}-{name}-provn">

In `PROV-N <http://www.w3.org/TR/prov-n/>`_ notation.

.. literalinclude:: {provnfile}

.. raw:: html

    </div>
    </div>
""".strip()

ATTRIBUTE_TEMPLATE = """
``seis_prov:{name}`` {types}
    {description}
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
    entities = []
    for filename in json_files(folder=entity_dir):
        entities.append(create_rst_representation(filename))
    entities = "\n\n\n".join(entities)

    activities = []
    for filename in json_files(folder=activity_dir):
        activities.append(create_rst_representation(filename))
    activities = "\n\n\n".join(activities)

    with io.open(os.path.join(current_dir, "_generated_details.rst"), "wt") as fh:
        fh.write(DETAILS_TEMPLATE.format(
            entities=entities,
            activities=activities))


def create_rst_representation(json_file):
    with io.open(json_file, "rt") as fh:
        data = json.load(fh)
    node_type = os.path.basename(os.path.dirname(json_file))
    # Do the attributes first.
    attributes = []
    for attrib in data["attributes"]:
        attributes.append(ATTRIBUTE_TEMPLATE.format(
            name=attrib["name"],
            types=", ".join("**%s**" % _i for _i in attrib["types"]),
            description=attrib["description"]))

    attributes = "\n\n".join(attributes)
    title = "%s:%s" % (NS_PREFIX, data["name"])

    text = TEMPLATE.format(
        title=title,
        title_line="^" * len(title),
        description=data["description"],
        two_letter_code=data["two_letter_code"],
        label=data["recommended_label"],
        attributes=attributes,
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
        name=data["name"])

    return text


if __name__ == "__main__":
    create_details_rst()
