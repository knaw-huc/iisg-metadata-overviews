#!/usr/bin/python3

from sickle import Sickle
import csv
from lxml import etree
from datetime import datetime

# Initialize an OAI interface
sickle = Sickle('http://api.socialhistoryservices.org/solr/all/oai')
response = sickle.ListIdentifiers(metadataPrefix='marcxml', set='iish.evergreen.biblio', ignore_deleted=True)
# sickle = Sickle('https://evergreen.iisg.amsterdam/opac/extras/oai/biblio')
# response = sickle.ListIdentifiers(metadataPrefix='marcxml', ignore_deleted=True)

amount = 0 # if 0, than all records are handled

# export records
file_name = "identifiers.csv"
with open(file_name, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    for record in response:
        root = etree.XML(str(record))
        identifier = root.findtext("{http://www.openarchives.org/OAI/2.0/}identifier")
        datestamp  = root.findtext("{http://www.openarchives.org/OAI/2.0/}datestamp")
        now = datetime.now()
        writer.writerow([identifier, datestamp, now])
        amount = amount - 1
        if amount == 0: break 

print('done')