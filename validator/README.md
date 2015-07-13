# SEIS-PROV Validator

This module serves to validate `SEIS-PROV` files to
ensure consistency and compatibility between implementations.

## Installation

Python versions 2.7 and 3.4 have been tested; others might well work.
Additional required Python modules are:

* `prov`
* `jsonschema>=2.4.0`


Cloning the repository is currently necessary:

```bash
$ git clone https://github.com/SeismicData/SEIS-PROV.git
$ cd SEIS-PROV/validator
$ pip install -v -e .
```

## Usage

The module will install a single command: `seis-prov-validate`.

```bash
$ seis-prov-validate prov.xml
Valid SEIS-PROV file
```

Any other output mean your file is not valid. The error messages should
hopefully give hints how to fix it.
