NS_PREFIX = "seis_prov"
NS_SEIS = (NS_PREFIX, "http://asdf.readthedocs.org/seis_prov/0.0/#")

from datetime import datetime
import glob
import inspect
import prov.constants
import prov.model
from prov import dot
import os


filename = os.path.abspath(inspect.getfile(inspect.currentframe()))
folder = os.path.dirname(filename)
dot_folder = os.path.join(folder, "dot")
xml_folder = os.path.join(folder, "xml")
if not os.path.exists(dot_folder):
    os.makedirs(dot_folder)
if not os.path.exists(xml_folder):
    os.makedirs(xml_folder)

for prov_file in glob.glob(os.path.join(folder, "*.py")):
    if prov_file == filename:
        continue

    with open(prov_file, "rt") as fh:
        content = fh.read()

    name = os.path.splitext(os.path.basename(prov_file))[0].strip(
        os.path.extsep)
    dot_filename = os.path.join(dot_folder, name + os.path.extsep + "dot")
    xml_filename = os.path.join(xml_folder, name + os.path.extsep + "xml")

    pr = prov.model.ProvDocument()
    pr.add_namespace(*NS_SEIS)

    exec(content)

    dot.prov_to_dot(pr, use_labels=True).write_dot(dot_filename)
    pr.serialize(xml_filename, format="xml")
