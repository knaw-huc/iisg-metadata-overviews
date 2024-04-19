# IISG metadata overviews

The purpose of this repository is to harvest and convert the archival and bibliographic metadata from the International Institute of Social History (IISG) (originating from the open OAI-endpoint) to a csv file, which can be used to create overviews, queries and reports.

These overviews serve the purpose of providing insights into the metadata, which can be used for: retrospective cleaning to improve consistency, understanding the contents (unique values, data type(s)) of a given MARC field, among others.

The tasks that can be done with this code are:
1. Harvest the OAI metadata endpoints (from XML to an initial tabular format) (1)
2. Converting the output of the initial tabular format to a readable .csv in which each row represents a "record" and each column represents a property (MARC field/subfield)
3. Generating overviews of the existing fields and their contents.
4. Querying the content of specific Marc field(s) (unique values, data types, etc.), 

The main users of this repository are the cataloguer(s) of the IISG.

## Mentions of responsibility
- This repository is a fork of the original repository to harvest and generate the initial tabular format, created by Ivo Zandhuis (https://github.com/ivozandhuis/iisg-cetl).
- Some parts of the harvesting and initial converter scripts were improved based on suggestions from Rik Hoekstra and Stefan Klut (KNAW Humanities Cluster).

--
(1) More information here: https://iisg.amsterdam/en/collections/using/machine-access?back-link=1. This code uses these OAI (Open Archives Initiative Protocol for Metadata Harvesting) end point: http://api.socialhistoryservices.org/solr/all/oai"