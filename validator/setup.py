from setuptools import setup

setup(
    name="seis_prov_validate",
    version="0.1",
    py_modules=["seis_prov_validate"],
    install_requires=["prov", "jsonschema>=2.4.0"],
    entry_points="""
        [console_scripts]
        seis-prov-validate=seis_prov_validate.validator:main
    """
)
