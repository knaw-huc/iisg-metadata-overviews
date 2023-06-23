#!/usr/bin/python3

from pathlib import Path
from saxonche import PySaxonProcessor

testamount = 0

# TODO: base handling on status.db instead of the availability of the file in extracted!!! 

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="ead2rico/xsl/ead2rico.xslt")

src_path = Path("extracted")
for src_file in src_path.glob("**/*.xml"):
    out_file = Path('transformed').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    testamount = testamount - 1
    if testamount == 0: break 
