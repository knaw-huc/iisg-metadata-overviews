#!/usr/bin/python3

import urllib.request
from pathlib import Path
from lxml import etree
from datetime import datetime

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
    if path.exists():
        for file in path.glob("**/*.xml"):
            mtime = file.stat().st_mtime
            file_last_mod_date = str(datetime.fromtimestamp(mtime).isoformat().split('T')[0])
            if last_mod_date < file_last_mod_date: last_mod_date = file_last_mod_date
    else:
        last_mod_date = "2000-01-01" # default

    return last_mod_date


# initialize
oai_endpoint          = "http://api.socialhistoryservices.org/solr/all/oai"
oai_identifier_prefix = "oai:socialhistoryservices.org:10622/"
oai_payload           = { 'verb': 'ListRecords',
                            'metadataPrefix': 'ead',
                            'set': 'iish.archieven' }
ext_path              = Path("extracted")
NS                    = { "oai": "http://www.openarchives.org/OAI/2.0/",
                          "ead": "urn:isbn:1-931666-22-9" }


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
        record = resource.find("oai:metadata//ead:ead", namespaces=NS)
        oai_identifier = resource.find("oai:header/oai:identifier", namespaces=NS).text
        identifier = oai_identifier.partition(oai_identifier_prefix)[2]
        file = ext_path.joinpath(to_balanced_path(identifier, '.xml', 6))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as xmlfile:
            xmlfile.write(etree.tostring(record, pretty_print=True).decode('utf-8'))
        print("written: " + str(file))

    resumption_token_element = root.find(".//oai:resumptionToken", namespaces=NS)
    if resumption_token_element is not None:
        oai_payload["resumptionToken"] = resumption_token_element.text
    else: break

print('done')
