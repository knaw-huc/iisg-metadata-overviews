#!/usr/bin/python3

import sqlite3

from sickle import Sickle
from lxml import etree
from pathlib import Path


def to_balanced_path(number: str, extension: str) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = number[3:][::-1]
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path


def get_process_list(status: str):
    # Get process_list of identifiers to be processed
    process_list = []
    con = sqlite3.connect("status.db")
    cur = con.cursor()
    for row in cur.execute('SELECT identifier FROM records WHERE status=?', status):
        process_list.append(row[0])
    con.close()
    print("process_list initiated. " + str(len(process_list)) + " items to be processed.")

    return process_list


# Initialize
url = 'http://api.socialhistoryservices.org/solr/all/oai'
oai_identifier_prefix = "oai:socialhistoryservices.org:iish.evergreen.authority:"

# url = 'https://evergreen.iisg.amsterdam/opac/extras/oai/authority'
# oai_identifier_prefix = "oai:evergreen.iisg.amsterdam:"

sickle = Sickle(url)
path = Path("extracted")
testamount = 0 # if 0, than all records are handled

process_list = get_process_list('c')

# Iterate identifiers
print("start extracting from " + url)

for identifier in process_list:
    oai_id = oai_identifier_prefix + identifier
    response = sickle.GetRecord(metadataPrefix='marcxml', identifier=oai_id)
    # how to handle errors from sickle?
    if response != "":
        root = etree.XML(str(response))
        metadata = root.find("{http://www.openarchives.org/OAI/2.0/}metadata")
        record = metadata.find("{http://www.loc.gov/MARC21/slim}record")
        file = path.joinpath(to_balanced_path(identifier, '.xml'))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))
    testamount = testamount - 1
    if testamount == 0: break 

print('done')