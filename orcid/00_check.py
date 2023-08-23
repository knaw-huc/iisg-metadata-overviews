#!/usr/bin/python3

import sqlite3
import csv
import datetime

import status_operations

amount = 0 # if 0, than all records are handled

# export records
file_name = "to_extract.csv"

status_operations.initiate_status_db()

con = sqlite3.connect("status.db") 
cur = con.cursor()

with open(file_name, "r", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        now = str(datetime.datetime.now().isoformat())
        status_record = (row[0], "c", now, "", "", "") 
        print(status_record)
        cur.execute("INSERT INTO records (identifier, status, last_check, last_extraction, last_transformation, last_load) VALUES (?, ?, ?, ?, ?, ?);", status_record)
        con.commit()
        amount = amount - 1
        if amount == 0: break 

con.close()
print('done')
status_operations.print_status_db()
