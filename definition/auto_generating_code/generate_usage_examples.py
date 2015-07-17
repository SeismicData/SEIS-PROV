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
            "example_cross_correlation",
            "example_adjoint_source"]


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

.. literalinclude:: _generated/py/examples/{filename}.py
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


if __name__ == "__main__":
    create_generated_details_rst()
