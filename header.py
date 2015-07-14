#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common definitions and functions for building the SEIS-PROV definition and
documentation.

:copyright:
    Lion Krischer (lion.krischer@geophysik.uni-muenchen.de), 2015
:license:
    The MIT License (MIT)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import inspect
import os

VERSION = "0.1"
NS_PREFIX = "seis_prov"
NS_URL = "http://seisprov.org/seis_prov/%s/#" % VERSION


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))

definitions_dir = os.path.join(current_dir, "definitions")
agent_dir = os.path.join(definitions_dir, "agents")
entity_dir = os.path.join(definitions_dir, "entities")
activity_dir = os.path.join(definitions_dir, "activities")
schema_filename = os.path.abspath(
    os.path.join(definitions_dir, "schema.json"))
generated_dir = os.path.join(current_dir, "_generated")
examples_dir = os.path.join(current_dir, "examples")

if not os.path.exists(generated_dir):
    os.makedirs(generated_dir)


def get_filename(filename, node_type, file_type, min_or_max=None):
    node_type = node_type.lower()
    file_type = file_type.lower()
    min_or_max = min_or_max.lower() if min_or_max else None

    assert node_type in ["activities", "entities", "agents", "examples"]
    assert file_type in ["xml", "dot", "py", "json", "provn"]
    assert min_or_max in ["min", "max", None]

    filename = os.path.splitext(os.path.basename(filename))[0]

    folder = os.path.join(generated_dir, file_type, node_type)
    if not os.path.exists(folder):
        os.makedirs(folder)

    if min_or_max:
        return os.path.join(folder, "%s_%s.%s" % (filename, min_or_max,
                                                  file_type))
    else:
        return os.path.join(folder, "%s.%s" % (filename, file_type))


def json_files(folder):
    """
    Generator yielding all JSON definition files as absolute paths.

    :param folder: Folder to recursively search into.
    """
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[-1].lower() != ".json":
                continue
            filename = os.path.abspath(os.path.join(dirpath, filename))
            if filename in [schema_filename]:
                continue
            yield filename
