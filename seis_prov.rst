Introduction to SEIS-PROV
=========================

W3C PROV
--------

``SEIS-PROV`` is a domain specific extension for using
`W3C PROV <http://www.w3.org/TR/prov-overview/>`_ in the context of
seismological data processing and generation.
``W3C PROV`` describes a generic data model for provenance which ``SEIS-PROV``
is based upon. Please see its website for more details. ``SEIS-PROV`` defines a
new namespace with entities and activities specific to seismology.

``W3C PROV`` offers a number of different serialization formats, all of which
are equivalent in their information content. The seismological community is
already used to XML with formats like QuakeML and StationXML so it makes sense
to use the `PROV-XML <http://www.w3.org/TR/prov-xml>`_ serialization to ease
adoption. Nonetheless you are free to use any serialization format you desire.

This section aims to give a short introduction to ``SEIS-PROV`` and ``W3C
PROV``.  Later sections will focus on the XML and graphical representations. We
will use examples familiar to seismologists where appropriate. The XML
representation is fairly verbose and tool support will be vital for its
success.

SEIS-PROV Namespace
-------------------

The namespace of the ``SEIS-PROV`` specific types and attributes will most
likely change at a certain point and should be considered temporary. Always use
the prefix |NS_PREFIX| to refer to it.

.. note::

    * **prefix:** |NS_PREFIX|
    * **namespace:** |NS_URL|

    The current version is |BOLDVERSION| and is not stable!

Approach to the Extension of W3C PROV
-------------------------------------

``W3C PROV`` in theory offers ways to properly extend it with new entity types
and relations. The downside of that approach is that most tools will not be
able to deal with. Since we strive towards a usable and practical provenance
description tool support is vital and should be facilitated by any means
possible.

``SEIS-PROV`` extends ``W3C PROV`` in a fairly non-intrusive fashion mainly by
adding new attributes to records under the |NS_PREFIX| namespace. This has the
big advantage of working with existing tools for ``W3C PROV``. The downside is
that no standard tools like XML schemas can be used to validate ``SEIS-PROV``
files. It follows that other ways to validate ``SEIS-PROV`` files are needed
which are detailed in a different section.


Provenance Records
------------------

``W3C PROV`` in essence describes a graph consisting of different types of
nodes, which are connected by different types of edges. There are three types
of nodes in ``W3C PROV`` which depict different things. The edges describe
different relations between the nodes.

We will first introduce the three different types, each with a short
description and a plot.


Entities
^^^^^^^^

.. sidebar:: Entity Plot

    .. graphviz:: _generated/dot/entities/waveform_trace_max.dot


    Entities are depicted as yellow ellipses. Attributes are listed in a white
    rectangle. This example show a waveform trace at a certain point in a
    processing chain.

An entity is an actual thing with some fixed aspects. In a seismological
context an entity is usually some piece of waveform or other data for which
provenance is described. In a time series analysis workflow for example the
data after each step in the processing chain will be described by an entity.

All ``SEIS-PROV`` entities are normal ``prov:entity`` records with a special
``prov:type`` attribute.

The most used entity in ``SEIS-PROV`` is the ``seis_prov:waveform_trace`` entity,
describing a single continuous piece of waveform data. ``SEIS-PROV`` furthermore defines
``seis_prov::cross_correlation``, ``seis_prov:cross_correlation_stack``,
and ``seis_prov:adjoint_source`` entities.
More entities will be added as the need arises.

Each type of entity has a set of (optional) attributes, the
``seis_prov:waveform_trace`` entity for example has attributes denoting the
network, station, location, and channel SEED identifies, the starttime,
sampling rate, the number of samples, and some more things.

In the PROV XML serialization the example in the small box results in the
following:

.. literalinclude:: _generated/xml/entities/waveform_trace_max.xml
    :language: xml


Activities
^^^^^^^^^^

.. sidebar:: Activity Plot

    .. graphviz:: _generated/dot/activities/lowpass_filter_max.dot

    Activities are shown as blue rectangles. The example shows a simple
    Butterworth lowpass filter.


Activities are action that can change or generate entities. In seismological
data processing, each processing step can be seen as an activity that uses the
data and generates a new version of the data.

A further example for an activity would be a simulation run which generates
some synthetic waveforms. Also an event relocation could be considered an
activity but that can also be stored in the QuakeML file directly, thus an
identifier which event was actually used should be enough. Model generation can
be considered an activity, as can adjoint backwards simulations to generate
gradients.

Activities can either use existing entities and generate new ones. The
``SEIS-PROV`` standard defines a number of activities from common processing
packages like SAC and ObsPy. Further activities should be added with time.
While it is not required we **strongly recommend** to associate each activity
with a software agent otherwise reproducibility is severely hurt.

A ``SEIS-PROV`` example for a simple lowpass filtered graphed in box above is given
in the following.

.. literalinclude:: _generated/xml/activities/lowpass_filter_max.xml
    :language: xml


Agents
^^^^^^

.. sidebar:: Agent Plot

    .. graphviz:: _generated/dot/examples/simple_agent.dot


    Agents are orange houses. The example shows a certain version of ObsPy.


Agents are persons, organizations, or software programs responsible for some
activity, entity, or another agent. One can define different relations between
the nodes. A classical example for an agent would be which software performed
the processing and which person steered the software. It could also be a group
of people or an institution.

``SEIS-PROV`` does not define any new agent types - the ones defined in ``W3C
PROV`` are sufficient. ``SEIS-PROV`` requires each software agent to have
``seis_prov:software_name``, ``seis_prov:sofware_version``, and
``seis_prov:website`` attributes. A human readable ``prov:label`` is
recommended. Agents can furthermore have an ``seis_prov:doi`` attribute.

The following example PROV XML serialization is the same as in the box above.

.. literalinclude:: _generated/xml/examples/simple_agent.xml
    :language: xml


Relations and the Rest of W3C PROV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``W3C PROV`` has a lot more to offer, everything can be used in ``SEIS-PROV``
but will not be described here - please refer to the ``W3C PROV`` specification
for more information.

The different types of records described in the previous sections are tied
together using relations. There are a number of relations in the ``W3C PROV``
data model, the important ones for ``SEIS-PROV`` are:

* ``Usage (used)``: Activities make use of entities, thus this is mostly used
  to note what entities or data went into an activity.
* ``Generation (wasGeneratedBy)``: Entities are generated by activities, thus
  this is mostly used to show the output of an activitiy.
* ``Association (wasAssociatedWith)``: Mostly used to show which agent is
  responsible for a certain activitiy, e.g. which software performed the
  filtering operation.
* ``Delegation (actedOnBehalfOf)``: Mostly used to show what person was
  responsible for steering a piece of software.

If that is confusing it should be clearer by looking at the examples at the end
of this page.
