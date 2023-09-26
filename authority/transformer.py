#!/usr/bin/python3
# Transforms files in /extracted/ from MARCXML into Schema.org (RDF/XML)

from pathlib import Path
from saxonche import PySaxonProcessor

amount = 0 # if 0, than all records are handled

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="auth2sdo.xsl")

ext_path = Path("extracted_test")
for src_file in ext_path.glob("**/*.xml"):
    out_file = Path('transformed_test').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    amount = amount - 1
    if amount == 0: break 

print('done')