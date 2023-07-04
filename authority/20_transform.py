#!/usr/bin/python3

from pathlib import Path
from saxonche import PySaxonProcessor, PyXdmValue, PyXdmItem

testamount = 3

# TODO: base handling on status.db instead of the availability of the file in extracted!!! 

xqproc = PySaxonProcessor(license=False).new_xquery_processor()
xq_file = "marcauth-to-madsrdf/process/saxon.xqy"
# xq_file = "process/saxon.xqy"

src_path = Path("extracted")
for src_file in src_path.glob("**/*.xml"):
    out_file = Path('transformed').joinpath(*src_file.parts[1:])
    out_file = out_file.with_suffix('.rdf')
    out_file.parent.mkdir(parents=True, exist_ok=True)
    src_file_xdm = PySaxonProcessor(license=False).make_string_value(str(src_file))
    model_xdm = PySaxonProcessor(license=False).make_string_value('all')
    xqproc.set_parameter("marcxmluri", src_file_xdm)
    xqproc.set_parameter("model", model_xdm)
    xqproc.run_query_to_file(query_file=xq_file, 
                             output_file_name=str(out_file))

    print("written: " + str(out_file))
    testamount = testamount - 1
    if testamount == 0: break 
