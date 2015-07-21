obspy = pr.agent("seis_prov:sp001_sa_9dig8ata", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "SoftwareAgent")),
    ("prov:label", "ObsPy"),
    ("seis_prov:software_name", "ObsPy"),
    ("seis_prov:software_version", "0.10.1"),
    ("seis_prov:website", "http://www.obspy.org"),
    ("seis_prov:doi", "10.1785/gssrl.81.3.530"))
)

trace_1 = pr.entity("seis_prov:sp002_wf_4390jsdfj", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:seed_id", "BW.FURT.00.BHZ"),
    ("seis_prov:start_time",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(6000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)

trace_2 = pr.entity("seis_prov:sp003_wf_0034aiddj8", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:seed_id", "BW.ALTM..BHZ"),
    ("seis_prov:start_time",
     prov.model.Literal(datetime(2013, 1, 2, 12, 10, 11),
                        prov.constants.XSD_DATETIME)),
    ("seis_prov:number_of_samples",
     prov.model.Literal(6000, prov.constants.XSD_INT)),
    ("seis_prov:sampling_rate",
     prov.model.Literal(100.0, prov.constants.XSD_DOUBLE)),
    ("seis_prov:units", "m/s")
    )
)

cross_correlate = pr.activity("seis_prov:sp004_co_f87sf7sf78", other_attributes=(
    ("prov:label", "Cross Correlate"),
    ("prov:type", "seis_prov:cross_correlate"),
    ("seis_prov:correlation_type", "Phase Cross Correlation"),
    ("seis_prov:max_lag_time_in_sec", 120.0)
))

correlation = pr.entity("seis_prov:sp005_cc_utakgh82hl", other_attributes=(
    ("prov:label", "Cross Correlation"),
    ("prov:type", "seis_prov:cross_correlation"),
    ("seis_prov:correlation_type", "Phase Cross Correlation"),
    ("seis_prov:seed_id_a", "BW.FURT.00.BHZ"),
    ("seis_prov:seed_id_b", "BW.ALTM..BHZ"),
    ("seis_prov:max_correlation_coefficient", 0.75),
    ("seis_prov:max_lag_time_in_sec", 120.0)
))

pr.association(cross_correlate, obspy)

pr.usage(cross_correlate, trace_1)
pr.usage(cross_correlate, trace_2)

pr.generation(correlation, cross_correlate)
