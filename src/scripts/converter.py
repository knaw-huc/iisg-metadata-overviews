#!/usr/bin/python3
# this script converts the data in the "transformed.csv" (in which each row is a MARC property from a record) 
# to a csv in which each row is a record and each column is a MARC property with subfield.
# written by Liliana Melgar

from pathlib import Path # iterates through all files
import pandas as pd
import numpy as np
import csv
import re
#to add timestamp to file names
import time
#import os.path to add paths to files
import os

# SET DATA DIRECTORIES
#################### SET DATA DIRECTORIES ##################
# switch between 'biblio', 'archive', 'authority', 'subjects' depending on what source you want to extract the metadata from
data_source = 'authority'
format_converted = 'per_field' #switch to 'per_subfield' if you are using that format, check documentation at the beginning of this script

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
print(f'Currently you are converting the transformed files in {data_source} using format {format_converted}')

# create directory
os.mkdir(data_converted_directory)

# register start time
start_time = time.time()
print("Note that this script takes approx. 1 hour to run")

# read csv as dataframe (path to the .csv file in the ./transformed folder)
# low_memory=False is needed because DtypeWarning: Columns (0) have mixed types"
df_v1 = pd.read_csv(f'{data_transformed_directory}/{data_source}_{format_converted}.gzip', sep="\t", header=None, names=['id','marc_field','value'], compression='gzip', low_memory=False)

# drop the first row because it contains the old column names
df_v2 = df_v1.iloc[1:]

# # to check counts before filling in empty values
# print(biblio_df_v2.info(verbose = True, show_counts = True))
# print(biblio_df_v2.head(100))

# make a copy
df_v3 = df_v2.reset_index(drop=True).copy()

# convert the transformed data into a csv where each column is a marc field/subfield
df_v4 = df_v3.pivot_table(index="id", columns="marc_field", values="value", aggfunc=lambda x: '¶'.join(x.dropna()))

# # to check counts before filling in empty values
# print(biblio_df_v4.info(verbose = True, show_counts = True))

df_v5 = df_v4.fillna("null")

# # inspect the dataframe before storing it
# print(biblio_df_v5.info(verbose = True, show_counts = True))
# print(biblio_df_v5.describe())
# print(biblio_df_v5.head(10))

# make a copy
df = df_v5.reset_index(drop=True).copy()

df.to_csv(f'{data_converted_directory}/{data_source}_as_csv_{format_converted}.gzip', sep = '\t', index = False, compression = 'gzip')

# print(biblio_df_v5.head(100))

# register end time
end_time = time.time()
total_time = end_time - start_time
print("done")
print("total_time:", total_time, "sec.")