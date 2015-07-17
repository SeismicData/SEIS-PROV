#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
:copyright:
    Lion Krischer (lion.krischer@googlemail.com), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
from setuptools import setup

long_description = """
Source code: https://github.com/SeismicData/SEIS-PROV

Documentation: http://seismicdata.github.io/SEIS-PROV/
""".strip()

setup(
    name="seis_prov_validate",
    version="0.1",
    license="BSD",
    description="Validator for SEIS-PROV documents",
    long_description=long_description,
    url="https://github.com/SeismicData/SEIS-PROV",
    author="Lion Krischer",
    author_email="lion.krischer@googlemail.com",
    packages=["seis_prov_validate"],
    package_data={
        "seis_prov_validate": ["schemas/*.xsd",
                               "schemas/*.json",
                               "test_data/valid_files/*.json",
                               "test_data/valid_files/*.xml",
                               "test_data/invalid_files/*.xml",
                               "test_data/invalid_files/*.json",
                               "test_data/invalid_files/*.txt"]
    },
    install_requires=["prov", "jsonschema>=2.4.0", "lxml", "pytest", "six"],
    entry_points="""
        [console_scripts]
        seis-prov-validate=seis_prov_validate.validator:main
    """,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: BSD License"
    ],
    keywords=["seismology", "provenance", "science", "waveform simulation",
              "data processing"]
)
