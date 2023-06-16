# CETL
These scripts: 

0. Check which records are created, updated or deleted.
1. Extract metadata from a collection management system.
2. Transform data into RDF
3. Load the result into an appropriate databasesystem

For instance: for biblio it Checks via the ListIdentifiers verb of OAI-PMH which bibliographical records are changed in Evergreen, Extracts the metadata with a GetRecord request on the OAI-PMH endpoint, Transforms it into RDF (TBD: test the BIBFRAME transformations of the LoC) and finally uploads the data into TriplyDB.

Other example: for ORCID it creates a list of all the relevant ORCIDs, Extracts the data via content negotiation on orcid.org, (does not need to transform, because it is already RDF) and creates a zip-file with the records that can be uploaded into Druid (TBD: access Druid through the API)

## Pattern
The pipeline is managed through a database 'status.db' with identifiers needed to download the records identified with these identifiers. The check-step finds the newly created, updated or deleted identifiers, stores the status of the processing and the timestamps of the moments the record is checked, extracted, transformed and loaded.

## Prerequisites
The scripts run in Python3 and need the following libraries:
- sqlite3
- os
- datetime
- pathlib
- csv
- json
- requests
- Sickle (OAI-PMH library)

## Check
The check script creates and updates the list of identifiers to be downloaded, for instance with the OAI-PMH verb ListIdentifiers. 

todo:
* how to update this list

## Extract
With the identifiers in the status.db we download the records record by record, for instance with the OAI-PMH verb GetRecord or content negotiation. 

The downloaded data is stored in files, a file for every record, named with the number of the identifier. Because the number of records could be huge (eg 1.2 million for the bibliographical data) we store them in a balanced directory structure based on the last three digits of the (numerical) identifier.

todo:
* how to incrementally update the data (instead of downloading everything everytime)

## Transform
TBD

## Load
TBD

