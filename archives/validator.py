#!/usr/bin/python3

from pathlib import Path
from lxml import etree

# Load the XML schema
# Improve the xsd: there are errors here now.
xmlschema = etree.XMLSchema(etree.parse('ead-iisg.xsd'))

amount = 5 # if 0, than all records are handled

ext_path = Path("extracted")
for src_file in ext_path.glob("**/*.xml"):
    tree = etree.parse(src_file)
    if not xmlschema.validate(tree):
        print("INvalid: " + str(src_file))
    else:
        print("Valid:   " + str(src_file))
    amount = amount - 1
    if amount == 0: break 

print('done')