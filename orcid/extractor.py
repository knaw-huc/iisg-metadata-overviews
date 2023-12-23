#!/usr/bin/python3

from pathlib import Path
import requests
import json

def to_balanced_path(number: str, extension: str, n: int = 3) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = number[n:][::-1]
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path

# initialize
base_uri        = 'https://orcid.org/'
headers         = {'accept': 'application/ld+json'}
ext_path        = Path("extracted")

# TODO: create a processlist with the needed orcids
# options: 
# - get them from wikidata
# - use the ORCID API?
# - get them from Pure?
process_list = []

# content negotiate data from the URIs contructed from the identifiers in process_list
for identifier in process_list:
    uri = base_uri + identifier
    print(uri)
    r = requests.get(uri, headers=headers)
    if r.status_code == 200:
        response = r.json()
        file = ext_path.joinpath(to_balanced_path(identifier, '.json', 16))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as jsonfile:
            jsonfile.write(json.dumps(response))
        print("written: " + str(file))

print('done')