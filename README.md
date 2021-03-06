[![Build Status](https://travis-ci.org/SeismicData/SEIS-PROV.svg?branch=master)](https://travis-ci.org/SeismicData/SEIS-PROV)

# SEIS-PROV Definition

This repository contains the sources to build the `SEIS-PROV` definition and
documentation. Additionally it contains a reference implementation of a
`SEIS-PROV` validator.

Rendered version of the definition: http://seismicdata.github.io/SEIS-PROV


## Structure

* `definition`: `SEIS-PROV` definition in form of a partially auto generated
  Sphinx documentation.
* `validator`: A reference implementation of a `SEIS-PROV` validator written in
  Python.

## How to Build the Documentation

The documentation should be built with Python 3. Additionally the following
modules are required to successfully build it:

* `sphinx`
* `sphinx_rtd_theme`
* `colorama`
* `prov`
* `jsonschema`
* `lxml`
* `pydot` (On Python 3, install this: https://github.com/nlhepler/pydot/archive/master.zip)


Then it is simply a matter of

```bash
$ cd definition
$ make html
```

An HTML version of the documentation will be generated in
`definition/_build/html`.
