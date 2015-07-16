# SEIS-PROV Definition

This repository contains the sources to build the `SEIS-PROV` definition and
documentation. Additionally it contains a reference implementation of a
`SEIS-PROV` validator.


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

Then it is simply a matter of

```bash
$ cd definition
$ make html
```

An HTML version of the documentation will be generated in
`definition/_build/html`.
