# IISG CETL Authority

## Extractor
Gets the data from the OAI-PMH endpoint and writes it in `extracted`. This is done incrementally, based on the youngest date of change in a file in 'extracted'.

## Transformer
Transforms the extracted data in `extracted/` into RDF (from MARC to Schema.org) and writes it in `transformed/`.

### auth2sdo.xsl
XSLT stylesheets used to transform.

## Future work

### Needed additions
* Write a script to upload the result to a triple store, create a HDT file or something

### Potential additions
* validator.py
* patcher.py

Both writing yet another directory (called 'validated' and 'patched' respectively) with files.
