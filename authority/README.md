# authority
This CETL: 
0. Checks which records are created, updated or deleted.
1. Extracts bibliographical data from Evergreen through the socialhistory.org OAI-PMH in MarcXML format.
2. Transforms data into BIBFRAME with the XSLT library of marc2bibframe2 from the LoC
3. Loads the result into TriplyDB (?)

## Pattern
The pipeline is managed through a database 'status.db' with identifiers needed to download the records identified with these identifiers. The check-step finds the newly created, updated or deleted identifiers, stores the status of the processing and the timestamps of the moments the record is checked, extracted, transformed and loaded.

## Check
The check script creates and updates the list of identifiers to be downloaded with the OAI-PMH verb ListIdentifiers. 

## Extract
With the identifiers in the status.db we download the records record by record with the OAI-PMH verb GetRecord. This circumvents the timeouts we experience on the endpoint: if the download stops, we do not need to start from beginning but continue were we left off. 

The downloaded data is stored in files, a file for every record, named with the number of the identifier. Because the number of records is huge (1.2 million) we store them in a balanced directory structure based on the last three digits of the (numerical) identifier.

## Transform
TBD

## Load
TBD

