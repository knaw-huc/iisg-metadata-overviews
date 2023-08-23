#!/usr/bin/python3
# Extracts records from OAI-PMH endpoint based on list identifiers in to_extract.txt

from sickle import Sickle
from pathlib import Path
from lxml import etree

def to_balanced_path(number: str, extension: str, n: int = 3) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = number[n:][::-1]
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path

# initialize
sickle          = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
oai_identifier_prefix = "oai:socialhistoryservices.org:10622/"
oai_payload     = {'metadataPrefix': 'ead',
                   'set': 'iish.archieven' }
ext_path        = Path("extracted")
to_extract_file = open("monitored/to_extract.txt", "r")
amount          = 0 # testing purposes, if 0, than all records are handled

# read process_list from to_extract.txt
process_list = []
for line in to_extract_file:
    process_list.append(line.rstrip())

# get record from OAI-PMH endpoint per identifier in process_list
for identifier in process_list:
    oai_payload['identifier'] = oai_identifier_prefix + identifier
    print("OAI-payload: " + str(oai_payload))

    try: 
        response = sickle.GetRecord(**oai_payload)
    except: 
        response = ""
        print("No results")

    if response != "":
        root = etree.XML(str(response))
        metadata = root.find("{http://www.openarchives.org/OAI/2.0/}metadata")
        record = metadata.find("{urn:isbn:1-931666-22-9}ead")
        file = ext_path.joinpath(to_balanced_path(identifier, '.xml', 6))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))

    amount = amount - 1
    if amount == 0: break 

print('done')
