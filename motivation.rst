Motivation
==========

What is Provenance?
-------------------


    *Provenance is information about entities, activities, and people involved
    in producing a piece of data or thing, which can be used to form
    assessments about its quality, reliability or trustworthiness.*  [W3C_PROV]_


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
data recording is metadata, but not provenance.


Why it matters
--------------

Provenance is a key step towards the goal of reproducible research. The final
result of many research projects are some papers describing methodology and
results. Due to many subjective choices greatly influencing the final result
many papers are essentially one off studies that cannot be reproduced.
Scientists need to be very disciplined if they aim for reproducible results.
This problem only intensifies with increasing amounts of data common in modern
research.

Provenance is in theory able to solve this by capturing all information that
went into producing a particular result. If we want to advance our science we
have to become better at tracking, storing, and exchanging it.


Goal of SEIS-PROV
-----------------

Our goal here is not full reproducibility as too many variables affect the
final result. Effects we do not aim to capture are for example floating point
math differences on different machines and compilers, errors in CPU operations,
and similar, hard to describe effects.

What we strive for with our provenance description is simple:

    **A scientists looking at data described by our provenance information should
    be able to tell what steps where taken to generate this particular piece of
    data.**

.. rubric:: Footnotes
.. [W3C_PROV] http://www.w3.org/TR/prov-overview/


