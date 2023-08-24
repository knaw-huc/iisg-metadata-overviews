#!/usr/bin/python3
# Gets a list of identifiers to be extracted from OAI endpoint

from sickle import Sickle
from pathlib import Path
from lxml import etree
from datetime import datetime

# initialize
sickle          = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
oai_payload     = {'metadataPrefix': 'ead',
                   'set': 'iish.archieven' }
ext_path        = Path("extracted")
to_extract_file = open("monitored/to_extract.txt", "a")
amount          = 0 # testing purposes, if 0, than all records are handled

# find out date of last check, if any
last_check_date = "2000-01-01"
for src_file in ext_path.glob("**/*.xml"):
    mtime = src_file.stat().st_mtime
    src_file_last_mod_date = str(datetime.fromtimestamp(mtime).isoformat().split('T')[0])
    if last_check_date < src_file_last_mod_date:
        last_check_date = src_file_last_mod_date
oai_payload['from'] = last_check_date
print("OAI-payload: " + str(oai_payload))

# harvest OAI-PMH endpoint
try:
    response = sickle.ListIdentifiers(**oai_payload)
except:
    response = []
    print("No results")

for record in response:
    root = etree.XML(str(record))
    identifier = root.findtext("{http://www.openarchives.org/OAI/2.0/}identifier")
    identifier_oai = identifier.split("/")[1]
    to_extract_file.write(identifier_oai + "\n")
    print(identifier_oai)
    amount = amount - 1
    if amount == 0: break

print('done')
