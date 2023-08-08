#!/usr/bin/python3

from sickle import Sickle
import sqlite3
from lxml import etree
from datetime import datetime

import status_operations

# initialize
sickle = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
oai_payload = {'metadataPrefix': 'marcxml',
               'set': 'iish.evergreen.authority' }
db = "status.db"
amount = 0 # if 0, than all records are handled

# find out date of last check, if any
con = sqlite3.connect(db) 
cur = con.cursor()
res = cur.execute("SELECT MIN(last_check) FROM records")    
last_check_ts = str(res.fetchone()[0])
if (last_check_ts != 'None'):   
    last_check_date = last_check_ts.split(' ')[0]
    oai_payload['from'] = last_check_date
print("OAI-call: " + str(oai_payload))

# find identifiers
## THING: this script starts to initiate if the database is empty, but does not if only a part of the identifiers are loaded
try: 
    response = sickle.ListIdentifiers(**oai_payload)
    for record in response:
        root = etree.XML(str(record))
        identifier = root.findtext("{http://www.openarchives.org/OAI/2.0/}identifier")
        identifier_oai = identifier.split(":")[3]
        tupel = (identifier_oai,)
        res = cur.execute("SELECT COUNT(status) FROM records WHERE identifier=?;", tupel)
        identifier_count = int(res.fetchone()[0])
        now = str(datetime.now())
        if  identifier_count > 0:
            print('Update ' + identifier_oai)
            cur.execute("UPDATE records SET status = 'c' WHERE identifier=?;", tupel)    
        else:
            status_record = (identifier_oai, "c", now, "", "", "") 
            print('Insert ' + identifier_oai)
            cur.execute("INSERT INTO records (identifier, status, last_check, last_extraction, last_transformation, last_load) VALUES (?, ?, ?, ?, ?, ?);", status_record)    
        con.commit()
        amount = amount - 1
        if amount == 0: break

    con.close()
    status_operations.update_status_db('c')
    print('done')

except:
    print("An exception occured.")

status_operations.print_status_db(db=db)
