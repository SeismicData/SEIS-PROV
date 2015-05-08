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

import inspect
import io
import json
import os

import colorama
import jsonschema


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


if __name__ == "__main__":
    for filename in json_files(folder=definitions_dir,
                               exclude_filenames=[schema_filename]):
        print(colorama.Fore.GREEN +
              "Validating %s ..." % os.path.relpath(filename) +
              colorama.Style.RESET_ALL)
        with io.open(filename, "rt") as fh:
            jsonschema.validate(json.load(fh), schema)
