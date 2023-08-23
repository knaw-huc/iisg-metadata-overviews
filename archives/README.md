# IISG CETL Archives

Principles: 
* All scripts are independent. You could run them in random order. Sometimes because the transformation script changed, sometimes because the data changed, sometimes both.
* If a script aborts inexpectately, the chain should not be broken. Calling it a new, makes it pick up were it left off.
* be generous with data storage so you could study all in between steps
* NOT: performance
* NOT: on-the-fly synchronization

## Monitor
See on the OAI-PMH endpoint whether changes are made to the data. Write a list of new data-records in `monitored/to_extract.txt`.

## Extractor
Gets the data, listed in `monitored/to_extract.txt`, from the OAI-PMH endpoint and writes it in `extracted`.

## Transformer
Transforms the extracted data in `extracted/` into RDF (from EAD to RiC-O) and writes it in `transformed/`.

### ead2rico
XSLT stylesheets used to transform.

## Loader
Shell script building a zip-file from the files in `transformed/`. The zip-file can be uploaded to druid (for now manually, automate it in the future)

## future work
Write a script `cleaner.py` that checks and cleans the bookkeeping

## Potential additions
* validator.py
* patcher.py

Both writing yet another directory (called 'validated' and 'patched' respectively) with files.