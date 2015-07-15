#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for the SEIS-PROV validator.

Execute with (require pytest to be installed):

$ py.test test_validator.py


:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
import glob
import inspect
import os
import pytest

from seis_prov_validate.validator import validate

# Most generic way to get the data folder path.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))), "test_data")

# Find all valid files.
VALID_FILES = {
    os.path.basename(_i): os.path.abspath(_i) for _i in
    glob.glob(os.path.join(DATA_DIR, "valid_files", "*.xml")) +
    glob.glob(os.path.join(DATA_DIR, "valid_files", "*.json"))}

# Make sure the globbing expression is not completely wrong.
assert len(VALID_FILES)

# Find all invalid files.
INVALID_FILES = {
    os.path.basename(_i): os.path.abspath(_i) for _i in
    glob.glob(os.path.join(DATA_DIR, "invalid_files", "*.xml")) +
    glob.glob(os.path.join(DATA_DIR, "invalid_files", "*.json"))}

# Make sure the globbing expression is not completely wrong.
assert len(INVALID_FILES)


@pytest.mark.parametrize("filename", sorted(VALID_FILES.values()))
def test_valid_files(filename):
    """
    Make sure all files that should be valid are valid.
    """
    assert validate(filename).is_valid is True


@pytest.mark.parametrize("filename", sorted(INVALID_FILES.values()))
def test_invalid_files(filename):
    """
    Make sure all files that should be invalid are invalid.
    """
    assert validate(filename).is_valid is False


def test_software_agent_missing_website():
    result = validate(INVALID_FILES["software_agent_missing_website.xml"])
    assert result.is_valid is False
    assert result.errors == [
        "Record 'seis_prov:sp001_sa_9345084' misses the following required "
        "attributes in the SEIS-PROV namespace: 'website'"]

    assert result.warnings == []


def test_software_agent_missing_multiple_attributes():
    result = validate(
        INVALID_FILES["software_agent_missing_multiple_attributes.xml"])
    assert result.is_valid is False
    assert result.errors == [
        "Record 'seis_prov:sp001_sa_9345084' misses the following required "
        "attributes in the SEIS-PROV namespace: 'software_name', "
        "'software_version', 'website'"]

    assert result.warnings == []


def test_non_existent_path():
    result = validate("some/random/path/that/does/not/exist")
    assert result.is_valid is False
    assert result.warnings == []
    assert result.errors == [
        "Path 'some/random/path/that/does/not/exist' does not exist."]


def test_validatig_folder():
    result = validate(DATA_DIR)
    assert result.is_valid is False
    assert result.warnings == []
    assert result.errors == [
        "Path '%s' is not a file." % DATA_DIR]
