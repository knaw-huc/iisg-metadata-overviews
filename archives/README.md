# IISG CETL Archives

## Monitor
See on the OAI-PMH endpoint whether changes are made to the data. Write a list of new data-records in `monitored/to_extract.txt`.

## Extractor
Gets the data, listed in `monitored/to_extract.txt`, from the OAI-PMH endpoint and writes it in `extracted`.

## Transformer
Transforms the extracted data in `extracted/` into RDF (from EAD to RiC-O) and writes it in `transformed/`.

### ead2rico
XSLT stylesheets used to transform.

## Future work

### Needed additions
* Write a script `cleaner.py` that checks and cleans the bookkeeping
* Write a script to upload the result to a triple store, create a HDT file or something

### Potential additions
* validator.py
* patcher.py

Both writing yet another directory (called 'validated' and 'patched' respectively) with files.