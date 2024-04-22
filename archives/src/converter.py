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
# this is the local path to the raw data in your own computer to where you downloaded/cloned the repository
# warning: the folders should be empty when starting this script
data_directory = os.path.abspath(os.path.join('..', 'data'))
data_extracted_directory = os.path.join(data_directory, 'extracted')
data_transformed_directory = os.path.join(data_directory, 'transformed')
data_converted_directory = os.path.join(data_directory, 'converted')

# register start time
start_time = time.time()

# read csv as dataframe (path to the .csv file in the ./transformed folder)
# low_memory=False is needed because DtypeWarning: Columns (0) have mixed types"
archives_df_v1 = pd.read_csv(f'{data_transformed_directory}/archives.csv', sep="\t", header=None, names=['id','marc_field','value'], compression='gzip', low_memory=False)

# drop the first row because it contains the old column names
archives_df_v2 = archives_df_v1.iloc[1:]

# # to check counts before filling in empty values
# print(archives_df_v2.info(verbose = True, show_counts = True))
# print(archives_df_v2.head(100))

# make a copy
archives_df_v3 = archives_df_v2.reset_index(drop=True).copy()

# convert the transformed data into a csv where each column is a marc field/subfield
archives_df_v4 = archives_df_v3.pivot_table(index="id", columns="marc_field", values="value", aggfunc=lambda x: 'Ω'.join(x.dropna()))

# # to check counts before filling in empty values
# print(archives_df_v4.info(verbose = True, show_counts = True))

archives_df_v5 = archives_df_v4.fillna("null")

# # inspect the dataframe before storing it
# print(archives_df_v5.info(verbose = True, show_counts = True))
# print(archives_df_v5.describe())
# print(archives_df_v5.head(10))

# make a copy
archives_df = archives_df_v5.reset_index(drop=True).copy()

archives_df.to_csv(f'{data_converted_directory}/archives_as_csv.csv', sep = '\t', index = False, compression = 'gzip')

# print(archives_df_v5.head(100))

# register end time
end_time = time.time()
total_time = end_time - start_time
print("done")
print("total_time:", total_time, "sec.")