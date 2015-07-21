trace_1 = pr.entity("seis_prov:sp001_wf_0439jdf", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
))

detrend = pr.activity("seis_prov:sp002_dt_f87sf7sf78", other_attributes=(
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean"),
))

trace_2 = pr.entity("seis_prov:sp003_wf_js83hf34aj", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
))


lowpass = pr.activity("seis_prov:sp004_lp_f87sf7sf78", other_attributes=(
    ("prov:label", "Lowpass Filter"),
    ("prov:type", "seis_prov:lowpass_filter"),
    ("seis_prov:filter_type", "Butterworth"),
    ("seis_prov:corner_frequency", 10.0),
    ("seis_prov:filter_order", 4),
    ("seis_prov:number_of_passes", 1),
))


trace_3 = pr.entity("seis_prov:sp005_wf_378f8ks8kd", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
))

decimate = pr.activity("seis_prov:sp006_dc_f87sf7sf78", other_attributes=(
    ("prov:label", "Decimate"),
    ("prov:type", "seis_prov:decimate"),
    ("seis_prov:factor", 2))
)

trace_4 = pr.entity("seis_prov:sp007_wf_jude89du8l", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
))

pr.usage(detrend, trace_1)
pr.usage(lowpass, trace_2)
pr.usage(decimate, trace_3)

pr.generation(trace_2, detrend)
pr.generation(trace_3, lowpass)
pr.generation(trace_4, decimate)
