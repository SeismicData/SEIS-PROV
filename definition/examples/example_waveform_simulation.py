me = pr.agent("seis_prov:sp000_pp_dj89345j", other_attributes=(
    ("prov:type",
        prov.identifier.QualifiedName(prov.constants.PROV, "Person")),
    ("prov:label", "Hans Mustermann"),
    ("seis_prov:name", "Hans Mustermann"),
    ("seis_prov:email", "hans.mustermann@email.com")
))

other = pr.agent("seis_prov:sp000_pp_9034j90df", other_attributes=(
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

model = pr.entity("seis_prov:sp000_em_skfusjdoej", other_attributes=(
    ("prov:label", "Earth Model"),
    ("prov:type", "seis_prov:earth_model"),
    ("seis_prov:model_name", "Random Model"),
    ("seis_prov:model_type", "3D"),
    ("seis_prov:website", "http://random.org/model")
))


param = pr.entity("seis_prov:sp000_in_38jd89da8l", other_attributes=(
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
    ("seis_prov:location", "/AuxiliaryData/Files/constants_h"),
    ("seis_prov:location_type", "HDF5 Data Set")
))


trace = pr.entity("seis_prov:sp001_wf_4j09fj3", other_attributes=(
    ("prov:label", "Waveform Trace"),
    ("prov:type", "seis_prov:waveform_trace"),
    ("seis_prov:description", "Synthetic Waveform")
))

simulation = pr.activity("seis_prov:sp001_ws_f87sf7sf78",
    startTime=datetime(2014, 2, 2, 12, 15, 3),
    endTime=datetime(2014, 2, 2, 14, 7, 13),
    other_attributes=(
    ("prov:label", "Waveform Simulation"),
    ("prov:type", "seis_prov:waveform_simulation"),
))


pr.association(simulation, specfem)
pr.association(model, other)
pr.delegation(specfem, me)

pr.usage(simulation, model)
pr.usage(simulation, param)
pr.usage(simulation, file_object)

pr.generation(trace, simulation)
