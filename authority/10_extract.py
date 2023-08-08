#!/usr/bin/python3

from sickle import Sickle
from lxml import etree
from pathlib import Path

import status_operations

# Initialize
sickle = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
oai_payload = {'metadataPrefix': 'marcxml',
               'set': 'iish.evergreen.authority' }
db = "status.db"
oai_identifier_prefix = "oai:socialhistoryservices.org:10622/"
path = Path("extracted")
amount = 10 # if 0, than all records are handled

process_list = status_operations.get_process_list_from_status_db('c')

# Iterate identifiers
for identifier in process_list:
    oai_id = oai_identifier_prefix + identifier
    oai_payload['identifier'] = oai_id
    print(oai_payload)
    response = sickle.GetRecord(**oai_payload)
    # how to handle errors from sickle?
    if response != "":
        root = etree.XML(str(response))
        metadata = root.find("{http://www.openarchives.org/OAI/2.0/}metadata")
        record = metadata.find("{http://www.loc.gov/MARC21/slim}record")
        file = path.joinpath(status_operations.to_balanced_path(identifier, '.xml', 6))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))
    amount = amount - 1
    if amount == 0: break 

print('done')
print('start updating status')
status_operations.update_status_db('e')
status_operations.print_status_db()