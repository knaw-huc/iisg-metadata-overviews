#!/usr/bin/python3

from sickle import Sickle
from lxml import etree
from pathlib import Path

import status_operations

# Initialize
url = 'http://api.socialhistoryservices.org/solr/all/oai'
oai_identifier_prefix = "oai:socialhistoryservices.org:10622/"

sickle = Sickle(url)
path = Path("extracted")
testamount = 0 # if 0, than all records are handled

process_list = status_operations.get_process_list_from_status_db('c')

# Iterate identifiers
print("start extracting from " + url)

for identifier in process_list:
    oai_id = oai_identifier_prefix + identifier
    response = sickle.GetRecord(metadataPrefix='ead', identifier=oai_id)
    # how to handle errors from sickle?
    if response != "":
        root = etree.XML(str(response))
        metadata = root.find("{http://www.openarchives.org/OAI/2.0/}metadata")
        record = metadata.find("{urn:isbn:1-931666-22-9}ead")
        file = path.joinpath(status_operations.to_balanced_path(identifier, '.xml', 6))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))
    testamount = testamount - 1
    if testamount == 0: break 

print('done')
status_operations.print_status_db()