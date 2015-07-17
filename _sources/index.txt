SEIS-PROV: Provenance for Seismological Data
============================================

.. image:: ./logo/seis_prov_logo.svg
    :width: 50%
    :align: center

.. note::

    While fairly fleshed out this is still a draft. Discuss any potential changes on
    `GitHub <https://github.com/SeismicData/SEIS-PROV>`_.

    Version of ``SEIS-PROV`` described in this document: |BOLDVERSION|

Welcome to the ``SEIS-PROV`` documentation and definition - a draft for a
standardized description of data history for seismology. This document is
organized as follows:


The first part introduces the concept of provenance and why it matters for our science.

.. toctree::
    :maxdepth: 2
    :glob:

    motivation


Following is a section with an introduction to ``W3C PROV`` and a high level
overview of the design of ``SEIS-PROV``.

.. toctree::
    :maxdepth: 2
    :glob:

    seis_prov


Subsequently the actual definitions are detailed.

.. toctree::
    :maxdepth: 2
    :glob:

    _generated_details


``SEIS-PROV`` documents must be validateable and verified to be correct to be
of any use. This section details this process and which steps must be
performed in order to make sure a given SEIS-PROV file is valid. It also
documents the usage of a reference implementation of a ``SEIS-PROV``
validator.

.. toctree::
    :maxdepth: 2
    :glob:

    validation


The final section illustrates some more complex use cases and scenarios.

.. toctree::
    :maxdepth: 2
    :glob:

    _generated_usage_examples
