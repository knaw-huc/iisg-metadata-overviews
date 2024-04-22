#!/usr/bin/python3
# Transforms files in /extracted/ from MARCXML into CSV
# Original script by Ivo Zandhuis, with adaptations to improve running time by Liliana Melgar (based on suggestions from Rik Hoekstra and Stefan Klut)

from pathlib import Path # iterates through all files
from lxml import etree
import pandas as pd
import time # to measure how long the process takes
import os # to define paths to folders

# register start time
start_time = time.time()

# SET DATA DIRECTORIES
# this is the local path to the raw data in your own computer to where you downloaded/cloned the repository
# warning: the folders should be empty when starting this script
data_directory = os.path.abspath(os.path.join('..', 'data'))
data_extracted_directory = os.path.join(data_directory, 'extracted')
data_transformed_directory = os.path.join(data_directory, 'transformed')
data_converted_directory = os.path.join(data_directory, 'converted')

amount = 0 # if 0, than all records are handled (this is for testing purposes, for not testing make it 0.

ext_path = Path(data_extracted_directory) # these are where the files are located
result_df = pd.DataFrame(columns = ['tcn', 'marcfield', 'value'])

# Extract relevant elements from each XML file and store them
dictionaries_list = []

for src_file in ext_path.glob("**/*.xml"): # for every file in extracted folder take all files ending in xml in directories and subdirectories
    record = etree.parse(src_file) # read the source file (xml) into an etree object
    tcn = record.find("{http://www.loc.gov/MARC21/slim}controlfield[@tag = '001']").text #find the tcn (Id) in the file using method "find", element controlfield with attribute tag equivalent to 001. Text extracts the value. This is an element defined in the MARC schema (namespace definition is used)
    leader = record.find("{http://www.loc.gov/MARC21/slim}leader")
    dictionary1 = {'tcn' : tcn, 'marcfield' : 'leader', 'value' : leader.text}
    dictionaries_list.append(dictionary1)
    for controlfield in record.findall(".//{http://www.loc.gov/MARC21/slim}controlfield"): #get a line for every field
        tag = controlfield.get("tag")
        dictionary2 = {'tcn' : tcn, 'marcfield' : tag, 'value' : controlfield.text}
        dictionaries_list.append(dictionary2)
    for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}datafield"): #iterate again over all data fields get value of attribute tag to get the subfields
        tag = datafield.get("tag")
        for subfield in datafield:
            code = subfield.get("code")
            dictionary3 = {'tcn' : tcn, 'marcfield' : tag + code, 'value' : subfield.text}
            dictionaries_list.append(dictionary3)
    amount = amount - 1
    if amount == 0: break

# create directory and store file
result_df = pd.DataFrame.from_dict(dictionaries_list)
result_df.to_csv(f"{data_transformed_directory}/archives.csv", sep = '\t', index = False, compression = 'gzip')

# register end time
end_time = time.time()
total_time = end_time - start_time
print("done")
print("total_time:", total_time, "sec.")