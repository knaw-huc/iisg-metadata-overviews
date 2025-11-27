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
print("Note that this script takes approx. 2,5 hours to run")

#################### SET DATA DIRECTORIES ##################
# switch between 'biblio', 'archive', 'authority', 'subjects' depending on what source you want to extract the metadata from
data_source = 'biblio'
format_converted = 'per_field' # check documentation at the beginning of this script

################# COMMON TO ALL DATA SOURCES ##################
# this is the local path to the raw data in your own computer to where you downloaded/cloned the repository
# warning: the folders should be empty when starting this script
script_dir = os.getcwd()  # Gets the current working directory
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))  # Moves up two levels to reach 'repo'
data_directory = os.path.join(project_root, "data", f"{data_source}")
data_extracted_directory = os.path.join(data_directory, 'extracted')
data_transformed_directory = os.path.join(data_directory, 'transformed')
data_converted_directory = os.path.join(data_directory, 'converted')

# MESSAGE WARNING WHERE YOU ARE HARVESTING
print(f'Currently you are transforming the extracted files from {data_source} using format {format_converted}')

######################## COMMON TO ALL DATA SOURCES ##################################################################

amount = 0 # if 0, than all records are handled (this is for testing purposes, for not testing make it 10 or something else.

ext_path = Path(data_extracted_directory) # these are where the files are located
# # create directory
os.mkdir(data_transformed_directory)
# create dataframe
result_df = pd.DataFrame(columns = ['tcn', 'marcfield', 'value'])

# Extract relevant elements from each XML file and store them
dictionaries_list = []

# store failed records
failed_files = []  # keep track of which records couldn't be processed

for src_file in ext_path.glob("**/*.xml"): # for every file in extracted folder take all files ending in xml in directories and subdirectories
    try:
        record = etree.parse(src_file) # read the source file (xml) into an etree object

        # try to extract tcn, but handle if it's missing
        tcn_elem = record.find("{http://www.loc.gov/MARC21/slim}controlfield[@tag = '001']")
        if tcn_elem is None or tcn_elem.text is None:
            raise ValueError("Missing or empty controlfield 001")

        tcn = tcn_elem.text
        leader = record.find("{http://www.loc.gov/MARC21/slim}leader")
        dictionary1 = {'tcn': tcn, 'marcfield': 'leader', 'value': leader.text if leader is not None else ""}
        dictionaries_list.append(dictionary1)

        for controlfield in record.findall(".//{http://www.loc.gov/MARC21/slim}controlfield"): #get a line for every field
            tag = controlfield.get("tag")
            dictionary2 = {'tcn': tcn, 'marcfield': tag, 'value': controlfield.text}
            dictionaries_list.append(dictionary2)

        for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}datafield"):
            tag = datafield.get("tag")
            subfield_values = [] # To collect all subfield values for this datafield
            for subfield in datafield:
                code = subfield.get("code")
                value = subfield.text
                subfield_values.append(f'"{code}":{value}')
            value_list_to_string = "⑄".join(str(element) for element in subfield_values)
            dictionary4 = {'tcn': tcn, 'marcfield': tag, 'value': value_list_to_string}
            dictionaries_list.append(dictionary4)

    except Exception as e:
        failed_files.append((src_file.name, str(e)))
        continue  # skip to the next file

if failed_files:
    print(f"\n⚠️ {len(failed_files)} files could not be processed:")
    for fname, err in failed_files:
        print(f"- {fname}: {err}")

    # # Optional: save to a log file
    # with open("failed_files.log", "w") as f:
    #     for fname, err in failed_files:
    #         f.write(f"{fname}\t{err}\n")

# create directory and store file
result_df = pd.DataFrame.from_dict(dictionaries_list)
# os.mkdir(data_transformed_directory)
result_df.to_csv(f"{data_transformed_directory}/{data_source}_{format_converted}.gzip", sep = '\t', index = False, compression = 'gzip')

# register end time
end_time = time.time()
total_time = end_time - start_time
print("done")
print("total_time:", total_time, "sec.")