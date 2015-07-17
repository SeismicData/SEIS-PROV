# Define all the agents.
me = pr.agent("seis_prov:sp000_pp_me09234j", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "Person")),
    ("prov:label", "Hans Mustermann"),
    ("seis_prov:name", "Hans Mustermann"),
    ("seis_prov:email", "hans.mustermann@email.com")
))

other = pr.agent("seis_prov:sp000_pp_j3j4loikj90", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "Person")),
    ("prov:label", "Susanna Musterfrau"),
    ("seis_prov:name", "Susanna Musterfrau"),
    ("seis_prov:email", "susanna.musterfrau@email.com")
))

specfem = pr.agent("seis_prov:sp000_sa_9dig8ata", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "SoftwareAgent")),
    ("prov:label", "SPECFEM3D GLOBE"),
    ("seis_prov:software_name", "SPECFEM3D GLOBE"),
    ("seis_prov:software_version", "7.0.0"),
    ("seis_prov:website", "http://geodynamics.org/cig/software/specfem3d")
))
# Specfem in this case has been steered by a certain person.
pr.delegation(specfem, me)

obspy = pr.agent("seis_prov:sp000_sa_9dig8ata", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "SoftwareAgent")),
    ("prov:label", "ObsPy"),
    ("seis_prov:software_name", "ObsPy"),
    ("seis_prov:software_version", "0.10.2"),
    ("seis_prov:website", "http://www.obspy.org"),
    ("seis_prov:doi", "10.5281/zenodo.17641"))
)

pyadjoint = pr.agent("seis_prov:sp000_sa_9d0h43a", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "SoftwareAgent")),
    ("prov:label", "pyadjoint"),
    ("seis_prov:software_name", "pyadjoint"),
    ("seis_prov:software_version", "0.0.1dev"),
    ("seis_prov:website", "http://krischer.github.io/pyadjoint"))
)


# Now everything needed to generate a synthetic waveform trace.
model = pr.entity("seis_prov:sp000_em_skfusjdoej", other_attributes=(
    ("prov:label", "Earth Model"),
    ("prov:type", "seis_prov:earth_model"),
    ("seis_prov:model_name", "Random Model"),
    ("seis_prov:model_type", "3D"),
    ("seis_prov:website", "http://random.org/model")
))
pr.association(model, other)

input_parameters = pr.entity("seis_prov:sp000_in_38jd89da8l", other_attributes=(
    ("prov:label", "Input Parameters"),
    ("prov:type", "seis_prov:input_parameters"),
    ("seis_prov:SIMULATION_TYPE", 1),
    ("seis_prov:NOISE_TOMOGRAPHY", 0),
    ("seis_prov:NCHUNKS", 1),
    ("seis_prov:ANGULAR_WIDTH_XI_IN_DEGREES", 90.0 ),
    ("seis_prov:ANGULAR_WIDTH_ETA_IN_DEGREES", 90.0),
    ("seis_prov:CENTER_LATITUDE_IN_DEGREES", 40.0),
    ("seis_prov:CENTER_LONGITUDE_IN_DEGREES", 10.0),
    ("seis_prov:GAMMA_ROTATION_AZIMUTH", 20.0),
    ("seis_prov:NEX_XI", 240),
    ("seis_prov:NEX_ETA", 240),
    ("seis_prov:NPROC_XI", 5),
    ("seis_prov:NPROC_ETA", 5),
    ("seis_prov:ANISOTROPIC_KL", False),
    ("seis_prov:RECEIVERS_CAN_BE_BURIED", True),
    ("seis_prov:USE_LDDRK", False),
    ("seis_prov:EXACT_MASS_MATRIX_FOR_ROTATION", False),
    ("seis_prov:ABSORBING_CONDITIONS", False),
    ("seis_prov:OCEANS", False),
    ("seis_prov:ELLIPTICITY", False),
    ("seis_prov:TOPOGRAPHY", False),
    ("seis_prov:GRAVITY", False),
    ("seis_prov:ROTATION", False),
    ("seis_prov:ATTENUATION", False)
))

file_object = pr.entity("seis_prov:sp000_fi_d49dh0h4", other_attributes=(
    ("prov:label", "File"),
    ("prov:type", "seis_prov:file"),
    ("seis_prov:filename", "constants.h"),
    ("seis_prov:location", "/AuxiliaryData/Files/constants.h"),
    ("seis_prov:location_type", "HDF5 Data Set")
))

simulation = pr.activity("seis_prov:sp001_ws_f87sf7sf78",
    startTime=datetime(2014, 2, 2, 12, 15, 3),
    endTime=datetime(2014, 2, 2, 14, 7, 13),
    other_attributes=(
    ("prov:label", "Waveform Simulation"),
    ("prov:type", "seis_prov:waveform_simulation"),
))
pr.association(simulation, specfem)

# This simulation used the model, the input parameters, and an additional
# files.
pr.usage(simulation, model)
pr.usage(simulation, input_parameters)
pr.usage(simulation, file_object)

synthetic_trace_N_original = pr.entity("seis_prov:sp001_wf_a34j4didj3", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))

synthetic_trace_E_original = pr.entity("seis_prov:sp001_wf_kd9404hd04h", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))

# And generated east and north synthetics.
pr.generation(synthetic_trace_N_original, simulation)
pr.generation(synthetic_trace_E_original, simulation)

# Now both synthetics will be detrended, demeaned, tapered, filtered, and once
# again everything.

# First detrend.
detrend_1_syn_N = pr.activity("seis_prov:sp002_dt_4ijf0dfo0", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_1_syn_N, obspy)
detrend_1_syn_E = pr.activity("seis_prov:sp002_dt_ir0dfk409", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_1_syn_E, obspy)

# First demean.
demean_1_syn_N = pr.activity("seis_prov:sp003_dt_4834f0dj0", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_1_syn_N, obspy)
demean_1_syn_E = pr.activity("seis_prov:sp003_dt_vj3urc943", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_1_syn_E, obspy)

# First taper
taper_1_syn_N = pr.activity("seis_prov:sp004_tp_dsfj43e4j", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_1_syn_N, obspy)
taper_1_syn_E = pr.activity("seis_prov:sp004_tp_dk430f834", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_1_syn_E, obspy)

# Pre filter.
pre_filt_syn_N = pr.activity("seis_prov:sp005_bp_qzprtj48r", other_attributes=((
    ("prov:label", "Bandpass Filter"),
    ("prov:type", "seis_prov:bandpass_filter"),
    ("seis_prov:filter_type", "Cosine SAC Taper"),
    ("seis_prov:sac_cosine_taper_frequency_limits",
     "0.013333333,0.016666667,0.037037037,0.044444444")
)))
pr.association(pre_filt_syn_N, obspy)
pre_filt_syn_E = pr.activity("seis_prov:sp005_bp_843ijdfskjgr", other_attributes=((
    ("prov:label", "Bandpass Filter"),
    ("prov:type", "seis_prov:bandpass_filter"),
    ("seis_prov:filter_type", "Cosine SAC Taper"),
    ("seis_prov:sac_cosine_taper_frequency_limits",
     "0.013333333,0.016666667,0.037037037,0.044444444")
)))
pr.association(pre_filt_syn_E, obspy)

# Second detrend.
detrend_2_syn_N = pr.activity("seis_prov:sp006_dt_893ndidh", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_2_syn_N, obspy)
detrend_2_syn_E = pr.activity("seis_prov:sp006_dt_jk340du34j", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_2_syn_E, obspy)

# Second demean.
demean_2_syn_N = pr.activity("seis_prov:sp007_dt_dko349dfj", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_2_syn_N, obspy)
demean_2_syn_E = pr.activity("seis_prov:sp007_dt_9djldfj", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_2_syn_E, obspy)

# Second taper
taper_2_syn_N = pr.activity("seis_prov:sp008_tp_iojdf9834j", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_2_syn_N, obspy)
taper_2_syn_E = pr.activity("seis_prov:sp008_tp_834jd0h", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_2_syn_E, obspy)

# Interpolation.
interpolation_syn_N = pr.activity("seis_prov:sp009_ip_iadsf3490j", other_attributes=((
    ("prov:label", "Interpolate"),
    ("prov:type", "seis_prov:interpolate"),
    ("seis_prov:interpolation_method", "weighted average slopes"),
    ("seis_prov:new_sampling_rate", prov.model.Literal(
        1.0,
        prov.constants.XSD_DOUBLE))
)))
pr.association(interpolation_syn_N, obspy)
interpolation_syn_E = pr.activity("seis_prov:sp009_ip_diajsdf80", other_attributes=((
    ("prov:label", "Interpolate"),
    ("prov:type", "seis_prov:interpolate"),
    ("seis_prov:interpolation_method", "weighted average slopes"),
    ("seis_prov:new_sampling_rate", prov.model.Literal(
        1.0,
        prov.constants.XSD_DOUBLE))
)))
pr.association(interpolation_syn_E, obspy)

rotate_syn = pr.activity("seis_prov:sp010_rt_asdfkj4034", other_attributes=((
    ("prov:label", "Rotate"),
    ("prov:type", "seis_prov:rotate"),
    ("seis_prov:method", "NE->RT")
)))
pr.association(rotate_syn, obspy)

# The final trace has been rotated to transverse.
final_synthetic_trace = pr.entity("seis_prov:sp010_wf_43ptb430df", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "T"),
    ("seis_prov:description", "Synthetic Data")
))

# Create a lot of in between trace.
synthetic_trace_E_1 = pr.entity("seis_prov:sp002_wf_asdklfj93ef", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_2 = pr.entity("seis_prov:sp003_wf_wasdf34439", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_3 = pr.entity("seis_prov:sp004_wf_ds934jdafkj", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_4 = pr.entity("seis_prov:sp005_wf_zdkja894dioj", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_5 = pr.entity("seis_prov:sp006_wf_349df9j0", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_6 = pr.entity("seis_prov:sp007_wf_ijd0934j0", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_7 = pr.entity("seis_prov:sp008_wf_idj30949j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_E_8 = pr.entity("seis_prov:sp009_wf_09j3kjdi", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_1 = pr.entity("seis_prov:sp002_wf_eioasdf0934j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_2 = pr.entity("seis_prov:sp003_wf_kajoi4309j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_3 = pr.entity("seis_prov:sp004_wf_ija09j43l", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_4 = pr.entity("seis_prov:sp005_wf_lkjaoi9034j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_5 = pr.entity("seis_prov:sp006_wf_3oijoi904j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_6 = pr.entity("seis_prov:sp007_wf_iajsdfje", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_7 = pr.entity("seis_prov:sp008_wf_oij09adfj", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))
synthetic_trace_N_8 = pr.entity("seis_prov:sp009_wf_jasdfj09032j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Synthetic Data")
))


# Now connect everything.

pr.usage(detrend_1_syn_E, synthetic_trace_E_original)
pr.generation(synthetic_trace_E_1, detrend_1_syn_E)

pr.usage(demean_1_syn_E, synthetic_trace_E_1)
pr.generation(synthetic_trace_E_2, demean_1_syn_E)

pr.usage(taper_1_syn_E, synthetic_trace_E_2)
pr.generation(synthetic_trace_E_3, taper_1_syn_E)

pr.usage(pre_filt_syn_E, synthetic_trace_E_3)
pr.generation(synthetic_trace_E_4, pre_filt_syn_E)

pr.usage(detrend_2_syn_E, synthetic_trace_E_4)
pr.generation(synthetic_trace_E_5, detrend_2_syn_E)

pr.usage(demean_2_syn_E, synthetic_trace_E_5)
pr.generation(synthetic_trace_E_6, demean_2_syn_E)

pr.usage(taper_2_syn_E, synthetic_trace_E_6)
pr.generation(synthetic_trace_E_7, taper_2_syn_E)

pr.usage(interpolation_syn_E, synthetic_trace_E_7)
pr.generation(synthetic_trace_E_8, interpolation_syn_E)

pr.usage(detrend_1_syn_N, synthetic_trace_N_original)
pr.generation(synthetic_trace_N_1, detrend_1_syn_N)

pr.usage(demean_1_syn_N, synthetic_trace_N_1)
pr.generation(synthetic_trace_N_2, demean_1_syn_N)

pr.usage(taper_1_syn_N, synthetic_trace_N_2)
pr.generation(synthetic_trace_N_3, taper_1_syn_N)

pr.usage(pre_filt_syn_N, synthetic_trace_N_3)
pr.generation(synthetic_trace_N_4, pre_filt_syn_N)

pr.usage(detrend_2_syn_N, synthetic_trace_N_4)
pr.generation(synthetic_trace_N_5, detrend_2_syn_N)

pr.usage(demean_2_syn_N, synthetic_trace_N_5)
pr.generation(synthetic_trace_N_6, demean_2_syn_N)

pr.usage(taper_2_syn_N, synthetic_trace_N_6)
pr.generation(synthetic_trace_N_7, taper_2_syn_N)

pr.usage(interpolation_syn_N, synthetic_trace_N_7)
pr.generation(synthetic_trace_N_8, interpolation_syn_N)

pr.usage(rotate_syn, synthetic_trace_N_8)
pr.usage(rotate_syn, synthetic_trace_E_8)
pr.generation(final_synthetic_trace, rotate_syn)

# Real data processing chain.

real_trace_N_original = pr.entity("seis_prov:sp001_wf_0askjdf0", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))

real_trace_E_original = pr.entity("seis_prov:sp001_wf_asdfoij0", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))

# Now both reals will be detrended, demeaned, tapered, filtered, and once
# again everything.

# First detrend.
detrend_1_real_N = pr.activity("seis_prov:sp001_dt_o3ijasdfuh", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_1_real_N, obspy)
detrend_1_real_E = pr.activity("seis_prov:sp001_dt_ij2390jdl", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_1_real_E, obspy)

# First demean.
demean_1_real_N = pr.activity("seis_prov:sp002_dt_3809adlkjo", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_1_real_N, obspy)
demean_1_real_E = pr.activity("seis_prov:sp002_dt_ij09328j", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_1_real_E, obspy)

# First taper
taper_1_real_N = pr.activity("seis_prov:sp003_tp_kio390jf", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_1_real_N, obspy)
taper_1_real_E = pr.activity("seis_prov:sp003_tp_aioj309j", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_1_real_E, obspy)

# Pre filter.
pre_filt_real_N = pr.activity("seis_prov:sp004_bp_lij09jel", other_attributes=((
    ("prov:label", "Bandpass Filter"),
    ("prov:type", "seis_prov:bandpass_filter"),
    ("seis_prov:filter_type", "Cosine SAC Taper"),
    ("seis_prov:sac_cosine_taper_frequency_limits",
     "0.013333333,0.016666667,0.037037037,0.044444444")
)))
pr.association(pre_filt_real_N, obspy)
pre_filt_real_E = pr.activity("seis_prov:sp004_bp_ijasdoij4l", other_attributes=((
    ("prov:label", "Bandpass Filter"),
    ("prov:type", "seis_prov:bandpass_filter"),
    ("seis_prov:filter_type", "Cosine SAC Taper"),
    ("seis_prov:sac_cosine_taper_frequency_limits",
     "0.013333333,0.016666667,0.037037037,0.044444444")
)))
pr.association(pre_filt_real_E, obspy)

# instrument correction
remove_response_N = pr.activity("seis_prov:sp005_rr_ddcc155", other_attributes=((
    ("prov:label", "Remove Response"),
    ("prov:type", "seis_prov:remove_response"),
    ("seis_prov:water_level", prov.model.Literal(
        600,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:input_units", "counts"),
    ("seis_prov:output_units", "m")
)))
pr.association(pre_filt_real_N, obspy)
remove_response_E = pr.activity("seis_prov:sp005_rr_asdf34034", other_attributes=((
    ("prov:label", "Remove Response"),
    ("prov:type", "seis_prov:remove_response"),
    ("seis_prov:water_level", prov.model.Literal(
        600,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:input_units", "counts"),
    ("seis_prov:output_units", "m")
)))
pr.association(pre_filt_real_E, obspy)

# Second detrend.
detrend_2_real_N = pr.activity("seis_prov:sp006_dt_as034lkjo", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_2_real_N, obspy)
detrend_2_real_E = pr.activity("seis_prov:sp006_dt_asdfoij4", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "linear fit")
)))
pr.association(detrend_2_real_E, obspy)

# Second demean.
demean_2_real_N = pr.activity("seis_prov:sp007_dt_340jdflioj", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_2_real_N, obspy)
demean_2_real_E = pr.activity("seis_prov:sp007_dt_inv3l90o", other_attributes=((
    ("prov:label", "Detrend"),
    ("prov:type", "seis_prov:detrend"),
    ("seis_prov:detrending_method", "demean")
)))
pr.association(demean_2_real_E, obspy)

# Second taper
taper_2_real_N = pr.activity("seis_prov:sp008_tp_io34oic83", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_2_real_N, obspy)
taper_2_real_E = pr.activity("seis_prov:sp008_tp_9304jlkmio", other_attributes=((
    ("prov:label", "Taper"),
    ("prov:type", "seis_prov:taper"),
    ("seis_prov:window_type", "Hanning"),
    ("seis_prov:taper_width", prov.model.Literal(
        0.05,
        prov.constants.XSD_DOUBLE)),
    ("seis_prov:side", "both")
)))
pr.association(taper_2_real_E, obspy)

# Interpolation.
interpolation_real_N = pr.activity("seis_prov:sp009_ip_i34j09d", other_attributes=((
    ("prov:label", "Interpolate"),
    ("prov:type", "seis_prov:interpolate"),
    ("seis_prov:interpolation_method", "weighted average slopes"),
    ("seis_prov:new_sampling_rate", prov.model.Literal(
        1.0,
        prov.constants.XSD_DOUBLE))
)))
pr.association(interpolation_real_N, obspy)
interpolation_real_E = pr.activity("seis_prov:sp009_ip_4309jlkjn", other_attributes=((
    ("prov:label", "Interpolate"),
    ("prov:type", "seis_prov:interpolate"),
    ("seis_prov:interpolation_method", "weighted average slopes"),
    ("seis_prov:new_sampling_rate", prov.model.Literal(
        1.0,
        prov.constants.XSD_DOUBLE))
)))
pr.association(interpolation_real_E, obspy)

rotate_real = pr.activity("seis_prov:sp010_rt_039jznwmp", other_attributes=((
    ("prov:label", "Rotate"),
    ("prov:type", "seis_prov:rotate"),
    ("seis_prov:method", "NE->RT")
)))
pr.association(rotate_real, obspy)

# The final trace has been rotated to transverse.
final_real_trace = pr.entity("seis_prov:sp011_wf_aj0934mjh", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "T"),
    ("seis_prov:description", "Observed Data")
))

# Create a lot of in between trace.
real_trace_E_1 = pr.entity("seis_prov:sp002_wf_asdjf043m", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_2 = pr.entity("seis_prov:sp003_wf_9034jfzq", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_3 = pr.entity("seis_prov:sp004_wf_w90jasdfh", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_4 = pr.entity("seis_prov:sp005_wf_j0asdfm9", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_5 = pr.entity("seis_prov:sp006_wf_wasdfjme", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_6 = pr.entity("seis_prov:sp007_wf_j09boija", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_7 = pr.entity("seis_prov:sp008_wf_jasdf943", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_8 = pr.entity("seis_prov:sp009_wf_wj9hljo", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_E_9 = pr.entity("seis_prov:sp010_wf_fijioj345", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "E"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_1 = pr.entity("seis_prov:sp002_wf_wlkjsdf094", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_2 = pr.entity("seis_prov:sp003_wf_wjasdf4380", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_3 = pr.entity("seis_prov:sp004_wf_ncbeirp", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_4 = pr.entity("seis_prov:sp005_wf_wkjasdfio", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_5 = pr.entity("seis_prov:sp006_wf_wjasd9043", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_6 = pr.entity("seis_prov:sp007_wf_jasdfh4", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_7 = pr.entity("seis_prov:sp008_wf_asdfj9043", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_8 = pr.entity("seis_prov:sp009_wf_niasdf043", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))
real_trace_N_9 = pr.entity("seis_prov:sp010_wf_9043594j", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:component", "N"),
    ("seis_prov:description", "Observed Data")
))

# Now connect everything.

pr.usage(detrend_1_real_E, real_trace_E_original)
pr.generation(real_trace_E_1, detrend_1_real_E)

pr.usage(demean_1_real_E, real_trace_E_1)
pr.generation(real_trace_E_2, demean_1_real_E)

pr.usage(taper_1_real_E, real_trace_E_2)
pr.generation(real_trace_E_3, taper_1_real_E)

pr.usage(pre_filt_real_E, real_trace_E_3)
pr.generation(real_trace_E_4, pre_filt_real_E)

pr.usage(remove_response_E, real_trace_E_4)
pr.generation(real_trace_E_5, remove_response_E)

pr.usage(detrend_2_real_E, real_trace_E_5)
pr.generation(real_trace_E_6, detrend_2_real_E)

pr.usage(demean_2_real_E, real_trace_E_6)
pr.generation(real_trace_E_7, demean_2_real_E)

pr.usage(taper_2_real_E, real_trace_E_7)
pr.generation(real_trace_E_8, taper_2_real_E)

pr.usage(interpolation_real_E, real_trace_E_8)
pr.generation(real_trace_E_9, interpolation_real_E)

pr.usage(detrend_1_real_N, real_trace_N_original)
pr.generation(real_trace_N_1, detrend_1_real_N)

pr.usage(demean_1_real_N, real_trace_N_1)
pr.generation(real_trace_N_2, demean_1_real_N)

pr.usage(taper_1_real_N, real_trace_N_2)
pr.generation(real_trace_N_3, taper_1_real_N)

pr.usage(pre_filt_real_N, real_trace_N_3)
pr.generation(real_trace_N_4, pre_filt_real_N)

pr.usage(remove_response_N, real_trace_N_4)
pr.generation(real_trace_N_5, remove_response_N)

pr.usage(detrend_2_real_N, real_trace_N_5)
pr.generation(real_trace_N_6, detrend_2_real_N)

pr.usage(demean_2_real_N, real_trace_N_6)
pr.generation(real_trace_N_7, demean_2_real_N)

pr.usage(taper_2_real_N, real_trace_N_7)
pr.generation(real_trace_N_8, taper_2_real_N)

pr.usage(interpolation_real_N, real_trace_N_8)
pr.generation(real_trace_N_9, interpolation_real_N)

pr.usage(rotate_real, real_trace_N_9)
pr.usage(rotate_real, real_trace_E_9)
pr.generation(final_real_trace, rotate_real)

calc_adjoint_source = pr.activity("seis_prov:sp011_ca_c7540fc", other_attributes=((
    ("prov:label", "Calculate Adjoint Source"),
    ("prov:type", "seis_prov:calculate_adjoint_source"),
    ("seis_prov:adjoint_source_type", "Time Frequency Phase")
)))
pr.association(calc_adjoint_source, pyadjoint)

pr.usage(calc_adjoint_source, final_real_trace)
pr.usage(calc_adjoint_source, final_synthetic_trace)

adjoint_source = pr.entity("seis_prov:sp012_as_cd84e87", other_attributes=((
    ("prov:label", "Adjoint Source"),
    ("prov:type", "seis_prov:adjoint_source"),
    ("seis_prov:adjoint_source_type", "Time Frequency Phase")
)))

pr.generation(adjoint_source, calc_adjoint_source)
