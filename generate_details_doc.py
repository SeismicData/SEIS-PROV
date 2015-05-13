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

.. graphviz:: {dotfile}

.. literalinclude:: {xmlfile}
    :language: xml
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
        title_line="_" * len(title),
        description=data["description"],
        two_letter_code=data["two_letter_code"],
        label=data["recommended_label"],
        attributes=attributes,
        dotfile=os.path.relpath(get_filename(
            json_file, node_type, "dot", "max")),
        xmlfile=os.path.relpath(get_filename(
            json_file, node_type, "xml", "max")))

    return text


if __name__ == "__main__":
    create_details_rst()
