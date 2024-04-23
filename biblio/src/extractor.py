#!/usr/bin/python3
# script written by Ivo Zandhuis (https://github.com/ivozandhuis/iisg-cetl)


import urllib.request
from pathlib import Path
from lxml import etree
from datetime import datetime
import time # to measure how long the process takes
import os # to define paths to folders

def to_balanced_path(number: str, extension: str, n: int = 3) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = number[n:][::-1]
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path


def oai_request(endpoint: str, payload: dict):
    url = endpoint
    first = True
    for key in payload:
        if first: 
            url = url + "?"
            first = False
        else: 
            url = url + "&"
        url = url + key + "=" + payload[key]
    
    print(url)

    result = urllib.request.urlopen(url)
    response = result.read().decode()

    return response


def find_youngest_file_date(path: Path):
    last_mod_date = "2000-01-01" # default
    if path.exists():
        for file in path.glob("**/*.xml"):
            mtime = file.stat().st_mtime
            file_last_mod_date = str(datetime.fromtimestamp(mtime).isoformat().split('T')[0])
            if last_mod_date < file_last_mod_date: last_mod_date = file_last_mod_date

    return last_mod_date


# initialize
start_time = time.time() # to store time of start

# SET DATA DIRECTORIES
# this is the local path to the raw data in your own computer to where you downloaded/cloned the repository
# warning: the folders should be empty when starting this script
data_directory = os.path.abspath(os.path.join('..', 'data'))
data_extracted_directory = os.path.join(data_directory, 'extracted')
data_transformed_directory = os.path.join(data_directory, 'transformed')
data_converted_directory = os.path.join(data_directory, 'converted')


# HARVESTER
oai_endpoint          = "http://api.socialhistoryservices.org/solr/all/oai"
oai_identifier_prefix = "oai:socialhistoryservices.org:"
oai_payload           = { 'verb': 'ListRecords',
                          'metadataPrefix': 'marcxml',
                          'set': 'iish.evergreen.biblio' }
ext_path              = Path(data_extracted_directory)
NS                    = { "oai": "http://www.openarchives.org/OAI/2.0/",
                          "marc": "http://www.loc.gov/MARC21/slim" }

from_date = find_youngest_file_date(ext_path)
if from_date != '2000-01-01':
    oai_payload["from"] = from_date

while True:

    try:
        response = oai_request(oai_endpoint, oai_payload)
    except:
        print("OAI error")
        break

    try: 
        root = etree.XML(response)
    except:
        print("Parse error XML")
        break

    resources = root.xpath('/oai:OAI-PMH/oai:ListRecords/oai:record', namespaces=NS)
    for resource in resources:
        status = resource.find("oai:header", namespaces=NS).get('status')
        if status == 'deleted': continue
        record = resource.find("oai:metadata//marc:record", namespaces=NS)
        oai_identifier = resource.find("oai:header/oai:identifier", namespaces=NS).text
        identifier = oai_identifier.partition(oai_identifier_prefix)[2]
        file = ext_path.joinpath(to_balanced_path(identifier, '.xml', 3))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))

    resumption_token_element = root.find(".//oai:resumptionToken", namespaces=NS)
    if resumption_token_element is not None:
        oai_payload["resumptionToken"] = resumption_token_element.text
    else: break

# END
end_time = time.time() # to store at what time it ended
total_time = end_time - start_time
 
print('done')
print("total_time:", total_time, "sec.")

## CHECK CORRECTNESS: move to the ..data/extracted folder and use this command in the terminal to count number of records: 
# find . -type f | wc -l
## the number of records should be ca.5400.
## for an exact number, see the counter at the bottom of the OAI call: https://api.socialhistoryservices.org/solr/all/oai?verb=ListRecords&metadataPrefix=marcxml&set=iish.archieven

