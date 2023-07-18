#!/usr/bin/python3

from sickle import Sickle
import sqlite3
from lxml import etree
from datetime import datetime

import status_operations

# initialize
sickle = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
oai_payload = {'metadataPrefix': 'ead',
               'set': 'iish.archieven' }
db = "status_test.db"
amount = 10 # if 0, than all records are handled
status_operations.initiate_status_db(db = "status_test.db")

con = sqlite3.connect(db) 
cur = con.cursor()

# find identifiers
response = sickle.ListIdentifiers(**oai_payload)
for record in response:
    root = etree.XML(str(record))
    identifier = root.findtext("{http://www.openarchives.org/OAI/2.0/}identifier")
    print(identifier)
    identifier = identifier.split("/")[1]
    now = str(datetime.now())
    status_record = (identifier, "c", now, "", "", "") 
    print(status_record)
    cur.execute("INSERT INTO records (identifier, status, last_check, last_extraction, last_transformation, last_load) VALUES (?, ?, ?, ?, ?, ?);", status_record)    
    con.commit()
    amount = amount - 1
    if amount == 0: break 

con.close()
print('done')
status_operations.print_status_db()