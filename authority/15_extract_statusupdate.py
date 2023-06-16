#!/usr/bin/python3

import sqlite3
import os
import datetime

def status_update(status: str):
    status_dict = {'e': 'extracted', 't': 'transformed'}
    path = status_dict[status] # add error handling!!
    con = sqlite3.connect("status.db")
    cur = con.cursor()
    for root, subdirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            identifier = filename.split('.')[0]
            mtime = os.path.getmtime(file_path)
            timestamp = datetime.datetime.fromtimestamp(mtime).isoformat()
            record = (status, timestamp, identifier)
            cur.execute('UPDATE records SET status = ?, last_extraction = ? WHERE identifier = ?', record)
            con.commit()
            print('status updated ' + str(record))

    con.close()


status_update('e')