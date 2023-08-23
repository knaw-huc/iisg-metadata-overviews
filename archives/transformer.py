#!/usr/bin/python3
# Transforms files in /extracted/ from EAD (XML) into RiC-O (RDF/XML)

from pathlib import Path
from saxonche import PySaxonProcessor

amount = 0 # if 0, than all records are handled

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="ead2rico/xsl/ead2rico.xslt")

# Potential improvement: only run transformation if both
# max last_mod_date in ead2rico/ > last_mod_date of the result in transformed/
# OR
# last_mod_date of a file in extracted/ > last_mod_date of the result in transformed/

ext_path = Path("extracted")
for src_file in ext_path.glob("**/*.xml"):
    out_file = Path('transformed').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    amount = amount - 1
    if amount == 0: break 

print('done')