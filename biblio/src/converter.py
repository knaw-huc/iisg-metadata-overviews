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

# create directory
os.mkdir(data_converted_directory)

# register start time
start_time = time.time()
print("Note that this script takes approx. 1 hour to run")

# read csv as dataframe (path to the .csv file in the ./transformed folder)
# low_memory=False is needed because DtypeWarning: Columns (0) have mixed types"
biblio_df_v1 = pd.read_csv(f'{data_transformed_directory}/biblio.gzip', sep="\t", header=None, names=['id','marc_field','value'], compression='gzip', low_memory=False)

# drop the first row because it contains the old column names
biblio_df_v2 = biblio_df_v1.iloc[1:]

# # to check counts before filling in empty values
# print(biblio_df_v2.info(verbose = True, show_counts = True))
# print(biblio_df_v2.head(100))

# make a copy
biblio_df_v3 = biblio_df_v2.reset_index(drop=True).copy()

# convert the transformed data into a csv where each column is a marc field/subfield
biblio_df_v4 = biblio_df_v3.pivot_table(index="id", columns="marc_field", values="value", aggfunc=lambda x: 'Ω'.join(x.dropna()))

# # to check counts before filling in empty values
# print(biblio_df_v4.info(verbose = True, show_counts = True))

biblio_df_v5 = biblio_df_v4.fillna("null")

# # inspect the dataframe before storing it
# print(biblio_df_v5.info(verbose = True, show_counts = True))
# print(biblio_df_v5.describe())
# print(biblio_df_v5.head(10))

# make a copy
biblio_df = biblio_df_v5.reset_index(drop=True).copy()

biblio_df.to_csv(f'{data_converted_directory}/biblio_as_csv.gzip', sep = '\t', index = False, compression = 'gzip')

# print(biblio_df_v5.head(100))

# register end time
end_time = time.time()
total_time = end_time - start_time
print("done")
print("total_time:", total_time, "sec.")