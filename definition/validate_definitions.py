#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script validating all JSON files that make up the SEIS-PROV definition.

That's right: It attempts to validate the JSON files that eventually make up
the SEIS-PROV definition that will then be used to validate SEIS-PROV files...
This might seem a bit paranoid but has already caught a number of subtle bugs
and automatically checking everything is necessary to have everything more or
less correct...

Requires Python 2.7 or 3.4 and the following non-standard library modules:

* colorama
* jsonschema

:copyright:
    Lion Krischer (lion.krischer@geophysik.uni-muenchen.de), 2015
:license:
    The MIT License (MIT)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import inspect
import io
import json
import os
import sys

import colorama
import jsonschema

sys.path.append(".")
from header import generated_dir  # NOQA


class ValidationError(Exception):
    pass


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
definitions_dir = os.path.join(current_dir, "definitions")

schema_filename = os.path.abspath(
    os.path.join(definitions_dir, "schema.json"))
with io.open(schema_filename, "rt") as fh:
    schema = json.load(fh)


def json_files(folder, exclude_filenames):
    """
    Generator yielding all JSON definition files as absolute paths.

    :param folder: Folder to recursively search into.
    :param exclude_filenames: List of absolute file paths to exclude.
    """
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[-1].lower() != ".json":
                continue
            filename = os.path.abspath(os.path.join(dirpath, filename))
            if filename in exclude_filenames:
                continue
            yield filename


def validate():
    two_letter_codes = collections.defaultdict(list)

    collective_definition = {
        "entities": {},
        "activities": {},
        "agents": {}}

    for filename in json_files(folder=definitions_dir,
                               exclude_filenames=[schema_filename]):
        print(colorama.Fore.GREEN +
              "Validating %s ..." % os.path.relpath(filename) +
              colorama.Style.RESET_ALL)
        with io.open(filename, "rt") as fh:
            data = json.load(fh)

        # Validate against the scheme.
        jsonschema.validate(data, schema)

        # Check that the filename corresponds to the node name and label.
        name = os.path.splitext(os.path.basename(filename))[0]
        if name != data["name"]:
            raise ValidationError(
                "File '%s': 'name' attribute '%s' does not correspond to the "
                "filename." % (os.path.relpath(filename), data["name"]))

        # Agents have an arbitrary label. Other record types not.
        if data["type"] == "agent":
            expected_label = "*"
        else:
            expected_label = " ".join([_i.capitalize()
                                       for _i in name.split("_")])

        if expected_label != data["label"]:
            raise ValidationError(
                "File '%s': 'label' attribute '%s' is not equal "
                "to the expected value '%s':" % (
                    os.path.relpath(filename), data["label"],
                    expected_label))

        # Collect the two letter codes.
        two_letter_codes[data["two_letter_code"]].append(filename)

        # Add to collective information.
        if data["type"] == "entity":
            key = "entities"
        elif data["type"] == "activity":
            key = "activities"
        elif data["type"] == "agent":
            key = "agents"
        else:
            raise NotImplementedError
        collective_definition[key][data["name"]] = data

        # Find duplicate attribute names.
        attr_names = [_i["name"] for _i in data["attributes"]]
        duplicates = set([i for i in attr_names
                          if sum([1 for a in attr_names if a == i]) > 1])
        if duplicates:
            raise ValidationError(
                "File '%s': Duplicate attributes: %s" % (
                    os.path.relpath(filename), duplicates))

    for key, value in two_letter_codes.items():
        if len(value) == 1:
            continue
        raise ValidationError(
            "Two letter code '%s' is used in %i files: %s" % (
                key, len(value), ", ".join(value)))

    jsonfile = os.path.join(generated_dir, "seis_prov.json")
    with io.open(jsonfile, "wt") as fh:
        json.dump(collective_definition, fh, indent=4, separators=(',', ': '),
                  sort_keys=True)


if __name__ == "__main__":
    validate()
