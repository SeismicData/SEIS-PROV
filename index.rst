Provenance for Seismological Data
=================================

.. contents:: Table of Contents
    :local:
    :depth: 2

Motivation
----------

What is Provenance?
^^^^^^^^^^^^^^^^^^^

    Provenance is information about entities, activities, and people involved
    in producing a piece of data or thing, which can be used to form
    assessments about its quality, reliability or trustworthiness.  [W3C_PROV]_


In a seismological context provenance can be seen as information about the
processes that created a particular piece of data. For synthetic waveforms the
provenance information describes which solver and settings therein were used to
generate it. When looking at processed seismograms the provenance has knowledge
about the different time series analysis steps that led to it.


Provenance information can be derived from different perspectives.
*Agent-centered provenance* describes what people where involved in the
creation of a particular piece of data. *Object-centered provenance* traces the
origins of data by tracking the different pieces of information that assembled
it.  *Process-centered provenance* finally captures the actions that were taken
to generate that particular piece of data.

For the following we will take the **process-centered** viewpoint as
essentially all data in seismology can be described by a succession of
different processing steps that created it.

Provenance is a kind of metainformation but there is metainformation that is
not considered to be provenance. For example the physical location of a seismic
data recording is metadata but not provenance.


Why it matters
^^^^^^^^^^^^^^

Provenance is a key step towards the goal of reproducible research. The final
result of many research projects are some papers describing methodology and
results. Due to many subjective choices greatly influencing the final result
many papers are essentially one off studies that cannot be reproduced.
Scientists need to be very disciplined if they aim for reproducible results.
This problem only intensifies with increasing amounts of data common in modern
research.

Provenance is in theory able to solve this by capturing all information that
went into producing a particular result.


Goal of the Seismological Provenance Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our goal here is not full reproducibility as too many variables affect the
final result. Effects we do not aim to capture are for example floating point
math difference on different machines and compilers, errors in CPU operations,
and similar, hard to describe effects.

What we strive for with our provenance description is simple:

**A scientists looking at data described by our provenance information should
be able to tell what steps where taken to generate this particular piece of
data.**



Introduction to SEIS PROV
-------------------------

.. danger::
    This is work in progress and in no way finalized yet. Its main purpose
    right now is to spark some discussion.

`W3C PROV <http://www.w3.org/TR/2013/NOTE-prov-overview-20130430/>`_ describes
a generic data model for provenance. It defines a number of different
serializations for this model. The seismological community is already used to
XML with formats like QuakeML and StationXML so makes sense to use the
`PROV-XML <http://www.w3.org/TR/prov-xml>`_ serialization to ease adoption.

*SEIS PROV* is the working name of a domain specific extension for using
*W3C PROV* in the context of seismological data processing and generation.

This section aims to give a short introduction to *SEIS PROV* and *W3C PROV*
with a focus on the XML and graphical representations. We will use examples
familiar to seismologists where appropriate. The XML representation is fairly
verbose and tool support will be vital for its success.

SEIS PROV Namespace
^^^^^^^^^^^^^^^^^^^

The namespace of the *SEIS PROV* specific types and attributes will most likely
change at a certain point and should be considered temporary. Always use the
prefix **seis_prov** to refer to it.

.. note::

    * **prefix:** ``seis_prov``
    * **namespace:** ``http://asdf.readthedocs.org/seis_prov/0.0/#``

    The current version is **0.0** and is not stable!

Approach to the Extension of W3C PROV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

W3C PROV in theory offers ways to properly extend it with new entity types and
relations. The downside of that approach is that most tools will not be able to
deal with. Since we strive towards a usable and practical provenance
description tool support is vital and should be facilitated by any means
possible.

*SEIS PROV* extends W3C PROV in a fairly non-intrusive fashion mainly by adding
new attributes to records under the **seis_prov** namespace. This has the big
advantage of working with existing tools for W3C PROV. The downside is that no
standard tools like XML schemas can be used to validate *SEIS PROV* files.


Provenance Records
^^^^^^^^^^^^^^^^^^

*W3C PROV* in essence describes a graph consisting of different types of nodes,
which are connected by different types of edges. There are three types of nodes
in *W3C PROV* which depict different things. The edges describe different
relations between the nodes.

We will first introduce of the three different types, each with a short
description, a plot, an XML example, and how they are used in SEIS PROV.


Entities
________

.. sidebar:: Entity Plot

    .. graphviz:: code/dot/entity_waveform_trace.dot


    Entities are depicted as yellow ellipses. Attributes are listed in white
    rectangle. This example show a waveform trace at a certain point in a
    processing chain.

An entity is an actual thing with some fixed aspects. In a seismological
context an entity is usually some piece of waveform or other data for which
provenance is described. In a time series analysis workflow for example the
data after each step in the processing chain will be described by an entity.

All *SEIS_PROV* entities are normal ``prov:entity`` records with a special
``prov:type`` attribute.

The most used entity in *SEIS PROV* is the ``seis_prov:waveform_trace`` entity,
describing a single continuous piece of waveform data. *SEIS PROV* furthermore defines
``seis_prov::cross_correlation``, ``seis_prov:cross_correlation_stack``,
and ``seis_prov:adjoint_source`` entities.
More entities will be added as the need arises.

Each type of entity has a set of (optional) attributes, the
``seis_prov:waveform_trace`` entity for example has attributes denoting the
network, station, location, and channel SEED identifies, the starttime,
sampling rate, the number of samples, and some more things.

In the PROV XML serialization the example in the small box results in the
following:

.. literalinclude:: code/xml/entity_waveform_trace.xml
    :language: xml


Activities
__________

.. sidebar:: Activity Plot

    .. graphviz:: ./code/dot/activity_lowpass.dot

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

Activities can either use existing entities and generate new ones. The *SEIS
PROV* standard defines a number of activities from common processing packages
like SAC and ObsPy. Further activities should be added with time. While it is
not required we **strongly recommend** to associate each activity with a
software agent otherwise reproducibility is severely hurt.

A SEIS PROV example for a simple lowpass filtered graphed in box above is given
in the following.

.. literalinclude:: code/xml/activity_lowpass.xml
    :language: xml


Agents
______

.. sidebar:: Agent Plot

    .. graphviz:: ./code/dot/simple_agent.dot


    Agents are orange houses. The example shows a certain version of ObsPy.


Agents are persons, organizations, or software programs responsible for some
activity, entity, or another agent. One can define different relations between
the nodes. A classical example for an agent would be which software performed
the processing and which person steered the software. It could also be a group
of people or an institution.

*SEIS PROV* does not define any new agent types - the ones defined in W3C PROV
are sufficient. *SEIS PROV* requires each software agent to have
``seis_prov:software_name``, ``seis_prov:sofware_version``, and
``seis_prov:website`` attributes. A human readable ``prov:label`` is
recommended. Agents can furthermore have an ``seis_prov:doi`` attribute.

The following example PROV XML serialization is the same as in the box above.

.. literalinclude:: code/xml/simple_agent.xml
    :language: xml


Relations and the Rest of W3C PROV
__________________________________

W3C PROV has a lot more to offer, everything can be used in *SEIS PROV* but
will not be described here - please refer to the W3C PROV specification for
more information.

The different types of records described in the previous sections are tied
together using relations. There are a number of relations in the W3C PROV data
model, the important ones for *SEIS PROV* are:

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


.. toctree::
    :maxdepth: 2

    index
    details
