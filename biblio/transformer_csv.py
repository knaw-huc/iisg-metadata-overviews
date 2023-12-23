#!/usr/bin/python3
# Transforms files in /extracted/ from MARCXML into CSV

from pathlib import Path # iterates through all files
from lxml import etree
import pandas as pd

amount = 10 # if 0, than all records are handled (this is for testing purposes, for not testing make it 0.

ext_path = Path("extracted_test") # these are where the files are located
result_df = pd.DataFrame(columns = ['tcn', 'marcfield', 'value'])

for src_file in ext_path.glob("**/*.xml"): # for every file in extracted folder take all files ending in xml in directories and subdirectories
    record = etree.parse(src_file) # read the source file (xml) into an etree object
    tcn = record.find("{http://www.loc.gov/MARC21/slim}controlfield[@tag = '001']").text #find the tcn (Id) in the file using method "find", element controlfield with attribute tag equivalent to 001. Text extracts the value. This is an element defined in the MARC schema (namespace definition is used)
    leader = record.find("{http://www.loc.gov/MARC21/slim}leader")
    row_to_append = pd.DataFrame([{'tcn' : tcn, 'marcfield' : 'leader', 'value' : leader.text}])
    result_df = pd.concat([result_df, row_to_append])
    for controlfield in record.findall("//{http://www.loc.gov/MARC21/slim}controlfield"): #get a line for every field
        tag = controlfield.get("tag")
        row_to_append = pd.DataFrame([{'tcn' : tcn, 'marcfield' : tag, 'value' : controlfield.text}]) 
        result_df = pd.concat([result_df, row_to_append])
    for datafield in record.findall("//{http://www.loc.gov/MARC21/slim}datafield"): #iterate again over all data fields get value of attribute tag to get the subfields
        tag = datafield.get("tag")
        for subfield in datafield:
            code = subfield.get("code")
            row_to_append = pd.DataFrame([{'tcn' : tcn, 'marcfield' : tag + code, 'value' : subfield.text}])
            result_df = pd.concat([result_df, row_to_append])
    amount = amount - 1
    if amount == 0: break 

    result_df.to_csv('transformed/biblio.csv', index = False)