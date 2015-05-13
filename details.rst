Detailed Definitions
--------------------

This section details the *SEIS PROV* types and expected attributes and
constraints.

.. contents::
    :local:
    :depth: 1

Common Properties
^^^^^^^^^^^^^^^^^
* All identifiers associated with *SEIS PROV* have to live in the ``seis_prov``
  namespace. The identifiers have to be unique and the recommended form of the
  identifiers, as a regular expression, is
  ``seis_prov:[a-z]{2}_[A-Z0-9-]{10}`` (``seis_prov:`` followed by a two
  letter description of the entity, activity, ..., followed by an underscore
  and 10 uppercase alphanumeric letters.). The two letter description has the
  purpose to yield a minimal descriptive identifier while still keeping its
  total length fairly short. The description of each record will note the
  recommended two letter code.
* It is recommended to add a human readable ``prov:label`` to each entity,
  activity, and agent. It enables the generation of more descriptive graphs
  which will most likely be the representation that is consumed by the end
  users.
* In an effort to reduce the amount of text or information to parse, stations
  are identified via their SEED identifier, e.g. the dot seperated network,
  station, location, and channel code (NET.STA.LOC.CHA). The computational
  power required to split the attributes again and it results in a more
  readable definition and PROV XML file.

Entities
^^^^^^^^

*SEIS_PROV* determines the type of entity via the ``prov:type`` attribute which
can be one of the following choices. Further types will be added as requested
by the community.

.. contents::
    :local:
    :depth: 1

seis_prov:waveform_trace
________________________

Represents a continuous, equally sampled observed or synthetic waveform trace.
Most attributes are optional and can be used to describe either very detailed
or fairly general provenance information.

============================ =======
Two letter ID code:          ``wf``
Recommended ``prov:label``   ``Waveform Trace``
============================ =======

**Attributes**

``seis_prov:station_id`` *xsd:string*
    The SEED identifier of the recording station.

``seis_prov:starttime`` *xsd:dateTime*
    The time of the first sample in UTC.

``seis_prov:number_of_samples`` *xsd:positiveInteger**
    The number of samples in the trace.

``seis_prov:sampling_rate`` *xsd:double*
    The sampling rate of the data.

``seis_prov:units`` *xsd:string*
    Units of the waveform data as a common abbreviation, e.g. ``m``, ``m/s``,
    ``nm/s^2``, ...

**Example**

.. graphviz:: code/dot/entity_waveform_trace.dot

.. literalinclude:: code/xml/entity_waveform_trace.xml
    :language: xml

seis_prov:cross_correlation
____________________________

A cross correlation between two stations A and B. Station metadata is not
recorded here as it is part of either SEED or StationXML files. Any previously
applied processing is also not part of the entity but rather of the entity used
by the activity generating this one.

============================ =======
Two letter ID code:          ``cc``
Recommended ``prov:label``   ``Cross Correlation``
============================ =======

**Attributes**

``seis_prov:correlation_type`` *xsd:string*
    The type of performed cross correlation as a string.

``seis_prov:max_lag_time_in_sec`` *xsd:double*
    The maximum lag time used during the calculation in seconds.

``seis_prov:max_correlation_coefficient`` *xsd:double*
    The maximum correlation coefficient.

``seis_prov:station_id_A`` *xsd:string*
    The SEED identifier of station A.

``seis_prov:station_id_B`` *xsd:string*
    The SEED identifier of station B.

**Example**

.. graphviz:: code/dot/entity_cross_correlation.dot

.. literalinclude:: code/xml/entity_cross_correlation.xml
    :language: xml


seis_prov:cross_correlation_stack
_________________________________

A stack of cross correlations.

============================ =======
Two letter ID code:          ``cs``
Recommended ``prov:label``   ``Cross Correlation Stack``
============================ =======

**Attributes**

``seis_prov:correlation_type`` *xsd:string*
    The type of performed cross correlations as a string. Only useful if the
    same for all cross correlations, otherwise that information must be stored
    in the provenance records of the single cross correlations.

``seis_prov:correlation_count`` *xsd:positiveInteger*
    The amount of cross correlations in the stack.

``seis_prov:stacking_method`` *xsd:string*
    A string describing the method used to create the stack.

``seis_prov:station_id_A`` *xsd:string*
    The SEED identifier of station A.

``seis_prov:station_id_B`` *xsd:string*
    The SEED identifier of station B.


**Example**

.. graphviz:: code/dot/entity_cross_correlation_stack.dot

.. literalinclude:: code/xml/entity_cross_correlation_stack.xml
    :language: xml



seis_prov:adjoint_source
________________________

One component of an adjoint source used in adjoint simulations. The location
can be specified either in geographical coordinates (WGS84) or as the SEED
identifier of the corresponding station. The definition of geographic
coordinates is the same as in StationXML. Any processing applied to the data
before the adjoint source has been calculated (window picking, filtering, ...)
has to be described by provenance records on the waveform entities.

============================ =======
Two letter ID code:          ``as``
Recommended ``prov:label``   ``Adjoint Source``
============================ =======

**Attributes**


``seis_prov:latitude`` *xsd:double*
    The latitude of the station in WGS84.

``seis_prov:longitude`` *xsd:double*
    The longitude of the station in WGS84.

``seis_prov:elevation_in_m`` *xsd:double*
    The elevation of the station in meter above the null level on WGS84.

``seis_prov:local_depth_in_m`` *xsd:double*
    The burial of the station in meter.

``seis_prov:orientation`` *xsd:string*
    The orientation of the adjoint source, either ``N`` (north),  ``E`` (east),
    ``Z`` (up), ``T`` (transverse), or ``R`` (radial). If that is not
    sufficient, please use the dip and azimuth attributes.

``seis_prov:dip`` *xsd:double*
    Dip of the component in degrees, down from horizontal, same definition as
    in StationXML.

``seis_prov:azimuth`` *xsd:double*
    Azimuth of the component in degrees from north, clockwise, same definition
    as in StationXML.

``seis_prov:station_id`` *xsd:string*
    The id of the recording station.

``seis_prov:number_of_samples`` *xsd:positiveInteger**
    The number of samples in the trace.

``seis_prov:sampling_rate`` *xsd:double*
    The sampling rate of the data.

``seis_prov:units`` *xsd:string*
    Units of the adjoint source as a common abbreviation, e.g. ``m``, ``m/s``,
    ``nm/s^2``, ...

``seis_prov:adjoint_source_type`` *xsd:string*
    A string denoting the type of adjoint source.

``seis_prov:adjoint_source_type_uri`` *xsd:anyURI*
    A URI pointing to a detailed description of the adjoint source, for example
    a DOI link to a publication.

``seis_prov:misfit_value`` *xsd:double*
    The calculation of many types of adjoint sources will automatically yield a
    misfit value denoting the similarity of usually observed and synthetic
    seismograms.

**Example**

.. graphviz:: code/dot/entity_adjoint_source.dot

.. literalinclude:: code/xml/entity_adjoint_source.xml
    :language: xml





Activities
^^^^^^^^^^

*SEIS_PROV* determines the type of activity via the ``prov:type`` attribute
which can be one of the following choices. Further types will be added as
requested by the community.

.. contents::
    :local:
    :depth: 1


seis_prov:decimate
__________________

Downsample the waveform data by an integer factor. Any applied anti-alias
filtering has to be described by a filtering activity.

============================ =======
two letter id code:          ``dc``
recommended ``prov:label``   ``Decimate``
============================ =======

**Attributes**

``seis_prov:factor`` *xsd:positiveInteger*
    The decimation factor.


**Example**

.. graphviz:: code/dot/activity_decimate.dot

.. literalinclude:: code/xml/activity_decimate.xml
    :language: xml



seis_prov:interpolate
_____________________

Interpolate the data to new sampling points.

============================ =======
two letter id code:          ``ip``
recommended ``prov:label``   ``Interpolate``
============================ =======

**Attributes**

``seis_prov:interpolation_method`` *xsd:string*
    The method used to interpolate the samples.

``seis_prov:new_starttime`` *xsd:dateTime*
    The new time of the first sample in UTC.

``seis_prov:new_number_of_samples`` *xsd:positiveInteger**
    The new number of samples in the trace.

``seis_prov:new_sampling_rate`` *xsd:double*
    The new sampling rate of the data.


**Example**

.. graphviz:: code/dot/activity_interpolate.dot

.. literalinclude:: code/xml/activity_interpolate.xml
    :language: xml


seis_prov:resample
__________________

Resample the data in the frequency domain.

============================ =======
two letter id code:          ``rs``
recommended ``prov:label``   ``Resample``
============================ =======

**Attributes**

``seis_prov:frequency_domain_window`` *xsd:string*
    The window applied to the signal in the Fourier domain.

``seis_prov:new_starttime`` *xsd:dateTime*
    The new time of the first sample in UTC.

``seis_prov:new_number_of_samples`` *xsd:positiveInteger**
    The new number of samples in the trace.

``seis_prov:new_sampling_rate`` *xsd:double*
    The new sampling rate of the data.


**Example**

.. graphviz:: code/dot/activity_resample.dot

.. literalinclude:: code/xml/activity_resample.xml
    :language: xml


seis_prov:detrend
_________________

Remove a trend from the data.

============================ =======
two letter id code:          ``dt``
recommended ``prov:label``   ``Detrend``
============================ =======

**Attributes**

``seis_prov:detrending_method`` *xsd:string*
    The method used to remove the trend from the data.


**Example**

.. graphviz:: code/dot/activity_detrend.dot

.. literalinclude:: code/xml/activity_detrend.xml
    :language: xml



seis_prov:differentiate
_______________________

Differentiate the data with respect to time.

============================ =======
two letter id code:          ``df``
recommended ``prov:label``   ``Differentiate``
============================ =======

**Attributes**

``seis_prov:differentiation_method`` *xsd:string*
    The method used to differentiate the data.


**Example**

.. graphviz:: code/dot/activity_differentiate.dot

.. literalinclude:: code/xml/activity_differentiate.xml
    :language: xml


seis_prov:integrate
___________________

Integrate the data with respect to time.

============================ =======
two letter id code:          ``in``
recommended ``prov:label``   ``Integrate``
============================ =======

**Attributes**

``seis_prov:integration_method`` *xsd:string*
    The method used to integrate the data.


**Example**

.. graphviz:: code/dot/activity_integrate.dot

.. literalinclude:: code/xml/activity_integrate.xml
    :language: xml


seis_prov:lowpass_filter
________________________

Lowpass the data.

============================ =======
two letter id code:          ``lp``
recommended ``prov:label``   ``Lowpass Filter``
============================ =======

**Attributes**

``seis_prov:filter_type`` *xsd:string*
    The type of filter, e.g. ``Butterworth``, ``FIR``, ``Chebyshev Type I/II``,
    ``Bessel``, ...

``seis_prov:corner_frequency`` *xsd:double*
    The corner frequency of the filter if applicable.

``seis_prov:filter_order`` *xsd:positiveInteger*
    The order of the filter if applicable.

``seis_prov:number_of_passes`` *xsd:positiveInteger*
    The number of filter passes if applicable.

``seis_prov:chebychev_transition_bw`` *xsd:double*
    The transition band with in the case of a Chebychev filter.

``seis_prov:chebychev_attenuation_factor`` *xsd:double*
    The attenuation factor in the case of a Chebychev filter.


**Example**

.. graphviz:: code/dot/activity_lowpass.dot

.. literalinclude:: code/xml/activity_lowpass.xml
    :language: xml


seis_prov:highpass_filter
_________________________

Highpass the data.

============================ =======
two letter id code:          ``hp``
recommended ``prov:label``   ``Highpass Filter``
============================ =======

**Attributes**

``seis_prov:filter_type`` *xsd:string*
    The type of filter, e.g. ``Butterworth``, ``FIR``, ``Chebyshev Type I/II``,
    ``Bessel``, ...

``seis_prov:corner_frequency`` *xsd:double*
    The corner frequency of the filter if applicable.

``seis_prov:filter_order`` *xsd:positiveInteger*
    The order of the filter if applicable.

``seis_prov:number_of_passes`` *xsd:positiveInteger*
    The number of filter passes if applicable.

``seis_prov:chebychev_transition_bw`` *xsd:double*
    The transition band with in the case of a Chebychev filter.

``seis_prov:chebychev_attenuation_factor`` *xsd:double*
    The attenuation factor in the case of a Chebychev filter.


**Example**

.. graphviz:: code/dot/activity_highpass.dot

.. literalinclude:: code/xml/activity_highpass.xml
    :language: xml


seis_prov:bandpass_filter
_________________________

Bandpass the data.

============================ =======
two letter id code:          ``bp``
recommended ``prov:label``   ``Bandpass Filter``
============================ =======

**Attributes**

``seis_prov:filter_type`` *xsd:string*
    The type of filter, e.g. ``Butterworth``, ``FIR``, ``Chebyshev Type I/II``,
    ``Bessel``, ...

``seis_prov:lower_corner_frequency`` *xsd:double*
    The lower corner frequency of the filter if applicable.

``seis_prov:upper_corner_frequency`` *xsd:double*
    The upper corner frequency of the filter if applicable.

``seis_prov:filter_order`` *xsd:positiveInteger*
    The order of the filter if applicable.

``seis_prov:number_of_passes`` *xsd:positiveInteger*
    The number of filter passes if applicable.

``seis_prov:chebychev_transition_bw`` *xsd:double*
    The transition band with in the case of a Chebychev filter.

``seis_prov:chebychev_attenuation_factor`` *xsd:double*
    The attenuation factor in the case of a Chebychev filter.


**Example**

.. graphviz:: code/dot/activity_bandpass.dot

.. literalinclude:: code/xml/activity_bandpass.xml
    :language: xml


seis_prov:bandstop_filter
_________________________

Bandstop the data.

============================ =======
two letter id code:          ``bs``
recommended ``prov:label``   ``Bandstop Filter``
============================ =======

**Attributes**

``seis_prov:filter_type`` *xsd:string*
    The type of filter, e.g. ``Butterworth``, ``FIR``, ``Chebyshev Type I/II``,
    ``Bessel``, ...

``seis_prov:lower_corner_frequency`` *xsd:double*
    The lower corner frequency of the filter if applicable.

``seis_prov:upper_corner_frequency`` *xsd:double*
    The upper corner frequency of the filter if applicable.

``seis_prov:filter_order`` *xsd:positiveInteger*
    The order of the filter if applicable.

``seis_prov:number_of_passes`` *xsd:positiveInteger*
    The number of filter passes if applicable.

``seis_prov:chebychev_transition_bw`` *xsd:double*
    The transition band with in the case of a Chebychev filter.

``seis_prov:chebychev_attenuation_factor`` *xsd:double*
    The attenuation factor in the case of a Chebychev filter.


**Example**

.. graphviz:: code/dot/activity_bandstop.dot

.. literalinclude:: code/xml/activity_bandstop.xml
    :language: xml


seis_prov:normalize
___________________

Normalize the data.

============================ =======
two letter id code:          ``nm``
recommended ``prov:label``   ``Normalize``
============================ =======

**Attributes**

``seis_prov:normalization_method`` *xsd:string*
    The type of normalization used. This is very implementation specific but
    useful to capture.


**Example**

.. graphviz:: code/dot/activity_normalize.dot

.. literalinclude:: code/xml/activity_normalize.xml
    :language: xml


seis_prov:divide
________________

Divide each value of the data by a certain factor. This is implied by many
operations but sometimes useful to capture in its own right.

============================ =======
two letter id code:          ``dv``
recommended ``prov:label``   ``Divide``
============================ =======

**Attributes**

``seis_prov:divisor`` *xsd:double*
    The used divisor.


**Example**

.. graphviz:: code/dot/activity_divide.dot

.. literalinclude:: code/xml/activity_divide.xml
    :language: xml


seis_prov:multiply
__________________

Multiply each value of the data with a certain factor. This is implied by many
operations but sometimes useful to capture in its own right.

============================ =======
two letter id code:          ``mp``
recommended ``prov:label``   ``Multiply``
============================ =======

**Attributes**

``seis_prov:factor`` *xsd:double*
    The multiplication factor.


**Example**

.. graphviz:: code/dot/activity_multiply.dot

.. literalinclude:: code/xml/activity_multiply.xml
    :language: xml


seis_prov:rotate
________________

Rotate multi-component data.

============================ =======
two letter id code:          ``ro``
recommended ``prov:label``   ``Rotate``
============================ =======

**Attributes**

This activity has no other attributes. The rotation angles are described by
input and output activities.


**Example**

.. graphviz:: code/dot/activity_rotate.dot

.. literalinclude:: code/xml/activity_rotate.xml
    :language: xml


seis_prov:taper
_______________

Apply a taper to the data.

============================ =======
two letter id code:          ``ta``
recommended ``prov:label``   ``Taper``
============================ =======

**Attributes**

``seis_prov:taper_type`` *xsd:string*
    The type of taper window.

``seis_prov:taper_width`` *xsd:double*
    The width of the taper at each end. Must be between 0.0 and 0.5.

``seis_prov:side`` *xsd:string*
    ``left``, ``right``, or ``both``. If not given, ``both`` can be assumed.


**Example**

.. graphviz:: code/dot/activity_taper.dot

.. literalinclude:: code/xml/activity_taper.xml
    :language: xml


seis_prov:remove_response
_________________________

Remove an instrument's response. This activity should use an entity that points
to the used response function and how that was calculated.

============================ =======
two letter id code:          ``rr``
recommended ``prov:label``   ``Remove Response``
============================ =======

**Attributes**

``seis_prov:input_units`` *xsd:string*
    The input units. Optional as it can also be defined at the entities going
    in.

``seis_prov:output_units`` *xsd:string*
    The output units. Optional as it can also be defined at the entities going
    out.

**Example**

.. graphviz:: code/dot/activity_remove_response.dot

.. literalinclude:: code/xml/activity_remove_response.xml
    :language: xml


seis_prov:simulate_response
___________________________

Add an instrument's response. This activity should use an entity that points to
the used response function and how that was calculated.

============================ =======
two letter id code:          ``sr``
recommended ``prov:label``   ``Simulate Response``
============================ =======

**Attributes**

``seis_prov:input_units`` *xsd:string*
    The input units. Optional as it can also be defined at the entities going
    in.

``seis_prov:output_units`` *xsd:string*
    The output units. Optional as it can also be defined at the entities going
    out.

**Example**

.. graphviz:: code/dot/activity_simulate_response.dot

.. literalinclude:: code/xml/activity_simulate_response.xml
    :language: xml


seis_prov:cut
_____________

Cut the data resulting in a shorter trace.

============================ =======
two letter id code:          ``cu``
recommended ``prov:label``   ``Cut``
============================ =======

**Attributes**

``seis_prov:new_starttime`` *xsd:dateTime*
    The time of the first sample after the cutting operation.

``seis_prov:new_endtime`` *xsd:dateTime*
    The time of the last sample after the cutting operation.


**Example**

.. graphviz:: code/dot/activity_cut.dot

.. literalinclude:: code/xml/activity_cut.xml
    :language: xml


seis_prov:pad
_____________

Pad the data resulting in a longer trace.

============================ =======
two letter id code:          ``pa``
recommended ``prov:label``   ``Pad``
============================ =======

**Attributes**

``seis_prov:new_starttime`` *xsd:dateTime*
    The time of the first sample after the padding operation.

``seis_prov:new_endtime`` *xsd:dateTime*
    The time of the last sample after the padding operation.

``seis_prov:pad_value`` *xsd:numerical*
    The padding value.


**Example**

.. graphviz:: code/dot/activity_pad.dot

.. literalinclude:: code/xml/activity_pad.xml
    :language: xml



seis_prov:merge
_______________

Merge several traces into one. This is very implementation dependent and thus
the activity should be associated with a software agent.

============================ =======
two letter id code:          ``me``
recommended ``prov:label``   ``Merge``
============================ =======

**Attributes**

``seis_prov:merging_strategy`` *xsd:string*
    A string describing the applied merging strategy.


**Example**

.. graphviz:: code/dot/activity_merge.dot

.. literalinclude:: code/xml/activity_merge.xml
    :language: xml


seis_prov:split
_______________

Split one trace into several. This is very implementation dependent and thus
the activity should be associated with a software agent.

============================ =======
two letter id code:          ``sp``
recommended ``prov:label``   ``Split``
============================ =======

**Attributes**

``seis_prov:splitting_strategy`` *xsd:string*
    A string describing the applied splitting strategy.


**Example**

.. graphviz:: code/dot/activity_split.dot

.. literalinclude:: code/xml/activity_split.xml
    :language: xml


seis_prov:cross_correlate
_________________________

Cross correlate data of two stations. This does not contain information about
the used data as that is captured by the incoming entities.

============================ =======
two letter id code:          ``co``
recommended ``prov:label``   ``Cross Correlate``
============================ =======

**Attributes**

``seis_prov:correlation_type`` *xsd:string*
    The type of performed cross correlation as a string.

``seis_prov:max_lag_time_in_sec`` *xsd:double*
    The maximum lag time used during the calculation in seconds.


**Example**

.. graphviz:: code/dot/activity_cross_correlate.dot

.. literalinclude:: code/xml/activity_cross_correlate.xml
    :language: xml


seis_prov:stack_cross_correlations
__________________________________

Stack a number of cross correlations.

============================ =======
two letter id code:          ``sc``
recommended ``prov:label``   ``Stack Cross Correlations``
============================ =======

**Attributes**

``seis_prov:stacking_method`` *xsd:string*
    A string describing the method used to create the stack.


**Example**

.. graphviz:: code/dot/activity_stack_cross_correlations.dot

.. literalinclude:: code/xml/activity_stack_cross_correlations.xml
    :language: xml



seis_prov:calculate_adjoint_source
__________________________________

Calculate an adjoint source.

============================ =======
two letter id code:          ``ca``
recommended ``prov:label``   ``Calculate Adjoint Source``
============================ =======

**Attributes**

``seis_prov:adjoint_source_type`` *xsd:string*
    A string denoting the type of adjoint source.

``seis_prov:adjoint_source_type_uri`` *xsd:anyURI*
    A URI pointing to a detailed description of the adjoint source, for example
    a DOI link to a publication.

**Example**

.. graphviz:: code/dot/activity_calculate_adjoint_source.dot

.. literalinclude:: code/xml/activity_calculate_adjoint_source.xml
    :language: xml


seis_prov:waveform_simulation
_____________________________

Generate data by running some numerical or analytic code. Must be associated
with one or more agents and use some entities to achieve a useful description.

============================ =======
two letter id code:          ``ws``
recommended ``prov:label``   ``Waveform Simulation``
============================ =======

**Attributes**

This activity has no other attributes.


**Example**

.. graphviz:: code/dot/activity_waveform_simulation.dot

.. literalinclude:: code/xml/activity_waveform_simulation.xml
    :language: xml



Usage Examples
--------------

This section shows some more extensive examples demonstrating that SEIS PROV
can be used to capture provenance for a wide of seismological relevant
applications. Keep in mind that these diagrams describe the history of some
piece of data, not a workflow.  The **arrows point towards the past**, e.g. to
the origin of the data.

.. note::
    `Right click -> View Image` to see graphs in more detail.

.. contents::
    :local:
    :depth: 1


Detailed Processing Chain
^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how a linear chain of signal processing routines can
be described.  The data has been detrended with a linear fit, then a
Butterworth lowpass filter has been applied and finally some integer decimation
has been performed. All of these operations where performed by a certain
version of ObsPy. Toolboxes can be adapted to provide this kind of provenance
fully automatic.

.. graphviz:: code/dot/example_detailed_processing_chain.dot


.. literalinclude:: code/xml/example_detailed_processing_chain.xml
    :language: xml

Schematic Processing Chain
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes not all information needs to be captured for a given application and
SEIS PROV is flexible enough to also allow a qualitative description of a
workflow. This is the same example as above but with less information. This
could be treated as a schema on how to process a large amount of data
independent of the used software and actual data.

.. graphviz:: code/dot/example_schematic_processing_chain.dot


.. literalinclude:: code/xml/example_schematic_processing_chain.xml
    :language: xml


Waveform Simulation
^^^^^^^^^^^^^^^^^^^

This fairly realistic example demonstrates how the waveform files resulting
from a numerical simulation can be described. This example does use some of the
more advanced future of the W3C PROV data model which are useful in many
contexts. Note that the waveform simulation activity has start- and endtimes
and that SPECFEM in this example actually has been steered by a certain person.

The amount of information to store has to be decided by the given application.
The general idea is to store those input file parameters that actually have an
effect on the output. It might also be useful to store information about the
machine is was run on in the provenance information but that is not shown here.

The implementation of this in a waveform solver is fairly simple by just using
an existing SEIS PROV XML file as a template and adjusting the information
dynamically. No need to incorporate an actual XML library.


.. graphviz:: code/dot/example_waveform_simulation.dot

.. literalinclude:: code/xml/example_waveform_simulation.xml
    :language: xml

Cross Correlation
^^^^^^^^^^^^^^^^^

.. graphviz:: code/dot/example_cross_correlation.dot

.. literalinclude:: code/xml/example_cross_correlation.xml
    :language: xml
