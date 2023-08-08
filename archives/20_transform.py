#!/usr/bin/python3

from pathlib import Path
from saxonche import PySaxonProcessor

import status_operations

amount = 0 # if 0, than all records are handled

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="ead2rico/xsl/ead2rico.xslt")

src_path = Path("extracted")
for src_file in src_path.glob("**/*.xml"):
    out_file = Path('transformed').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    amount = amount - 1
    if amount == 0: break 

print('start updating status')
# status_operations.update_status_db('t')
status_operations.print_status_db()