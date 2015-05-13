# SEIS-PROV Definition

This repository contains the sources to build the `SEIS-PROV` definitions and
documentation.


## Files

* `definitions/schema.json`: JSON Schema file for the entity and activity
  definitions.
* `validate_definitions.py`: Python script used to validate all entity and
  activity JSON definitions. It validates it against the schema and performs
  some other consistency and sanity checks.
