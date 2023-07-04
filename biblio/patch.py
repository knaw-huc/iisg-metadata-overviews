#!/usr/bin/python3

from pathlib import Path
from saxonche import PySaxonProcessor

testamount = 0

xsltproc = PySaxonProcessor(license=False).new_xslt30_processor()
executable = xsltproc.compile_stylesheet(stylesheet_file="patchers/patch_008.xsl")

src_path = Path("extracted")
for src_file in src_path.glob("**/804002.xml"):
    out_file = Path('patched').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.xml')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    executable.transform_to_file(source_file=str(src_file), output_file=str(out_file))

    print("written: " + str(out_file))
    testamount = testamount - 1
    if testamount == 0: break 
