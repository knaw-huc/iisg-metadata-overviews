#!/usr/bin/python3
# Transforms files in /extracted/ from MARCXML into CSV

from pathlib import Path
from lxml import etree

amount = 10 # if 0, than all records are handled

ext_path = Path("extracted_test")
for src_file in ext_path.glob("**/*.xml"):
    record = etree.parse(src_file)
    tcn = record.find("{http://www.loc.gov/MARC21/slim}controlfield[@tag = '001']").text
    leader = record.find("{http://www.loc.gov/MARC21/slim}leader")
    print(tcn + ";leader;" + leader.text)
    for controlfield in record.findall("//{http://www.loc.gov/MARC21/slim}controlfield"):
        tag = controlfield.get("tag")
        print(tcn + ";" + tag + ";" + controlfield.text)
    for datafield in record.findall("//{http://www.loc.gov/MARC21/slim}datafield"):
        tag = datafield.get("tag")
        for subfield in datafield:
            code = subfield.get("code")
            print(tcn + ";" + tag + code + ";" + subfield.text)
    amount = amount - 1
    if amount == 0: break 

