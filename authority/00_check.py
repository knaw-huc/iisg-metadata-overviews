#!/usr/bin/python3

from sickle import Sickle
import sqlite3
from lxml import etree
from datetime import datetime

# Initialize an OAI interface
sickle = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
response = sickle.ListIdentifiers(metadataPrefix='marcxml', set='iish.evergreen.authority', ignore_deleted=True)
# sickle = Sickle('https://evergreen.iisg.amsterdam/opac/extras/oai/authority')
# response = sickle.ListIdentifiers(metadataPrefix='marcxml', ignore_deleted=True)

con = sqlite3.connect("status.db") 
cur = con.cursor()

amount = 0 # if 0, than all records are handled

# export records
for record in response:
    root = etree.XML(str(record))
    identifier = root.findtext("{http://www.openarchives.org/OAI/2.0/}identifier")
    print(identifier)
    tcn = identifier.split(":")[3]
    now = str(datetime.now())
    status_record = (tcn, "c", now, "", "", "") 
    print(status_record)
    cur.execute("INSERT INTO records (identifier, status, last_check, last_extraction, last_transformation, last_load) VALUES (?, ?, ?, ?, ?, ?);", status_record)    
    con.commit()
    amount = amount - 1
    if amount == 0: break 

con.close()
print('done')