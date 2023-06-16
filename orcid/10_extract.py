#!/usr/bin/python3

from pathlib import Path
import requests
import json

import status_operations

base_uri = 'https://orcid.org/'
path = Path("extracted")
testamount = 0 # if 0, than all records are handled

process_list = status_operations.get_process_list_from_status_db('c')

headers = {'accept': 'application/ld+json'}
for identifier in process_list:
    uri = base_uri + identifier
    print(uri)
    r = requests.get(uri, headers=headers)
    if r.status_code == 200:
        response = r.json()
        file = path.joinpath(status_operations.to_balanced_path(identifier, '.json', 16))
        file.parent.mkdir(exist_ok=True, parents=True)
        with open(file, "w") as jsonfile:
            jsonfile.write(json.dumps(response))
        print("written: " + str(file))
