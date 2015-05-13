obspy = pr.agent("seis_prov:sa_9DIG8A-TA", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "SoftwareAgent")),
    ("prov:label", "ObsPy"),
    ("seis_prov:software_name", "ObsPy"),
    ("seis_prov:software_version", "0.10.1"),
    ("seis_prov:website", "http://www.obspy.org"),
    ("seis_prov:doi", "10.1785/gssrl.81.3.530"))
)

trace_1 = pr.entity("seis_prov:wf_A34J4DIDJ3", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:station_id", "BW.FURT.00.BHZ"),
    ("seis_prov:starttime",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(6000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)

detrend = pr.activity("seis_prov:dt_F87SF7SF78", other_attributes=(
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean"),
))

trace_2 = pr.entity("seis_prov:wf_JS83HF34AJ", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:station_id", "BW.FURT.00.BHZ"),
    ("seis_prov:starttime",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(6000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)


lowpass = pr.activity("seis_prov:lp_F87SF7SF78", other_attributes=(
    ("prov:label", "Lowpass Filter"),
    ("prov:type", "seis_prov:lowpass_filter"),
    ("seis_prov:filter_type", "Butterworth"),
    ("seis_prov:corner_frequency", 10.0),
    ("seis_prov:filter_order", 4),
    ("seis_prov:number_of_passes", 1),
))


trace_3 = pr.entity("seis_prov:wf_378F8KS8KD", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:station_id", "BW.FURT.00.BHZ"),
    ("seis_prov:starttime",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(6000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)

decimate = pr.activity("seis_prov:cd_F87SF7SF78", other_attributes=(
    ("prov:label", "Decimate"),
    ("prov:type", "seis_prov:decimate"),
    ("seis_prov:factor", 2))
)

trace_4 = pr.entity("seis_prov:wf_JUDE89DU8L", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:station_id", "BW.FURT.00.BHZ"),
    ("seis_prov:starttime",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(3000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)

pr.association(detrend, obspy)
pr.association(lowpass, obspy)
pr.association(decimate, obspy)

pr.usage(detrend, trace_1)
pr.usage(lowpass, trace_2)
pr.usage(decimate, trace_3)

pr.generation(trace_2, detrend)
pr.generation(trace_3, lowpass)
pr.generation(trace_4, decimate)
