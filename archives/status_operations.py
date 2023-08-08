import sqlite3
import os
from datetime import datetime
from pathlib import Path


def to_balanced_path(number: str, extension: str, n: int = 3) -> Path:
    # credit for this idea: https://www.linkedin.com/in/martijnschiedon
    parts = number[n:][::-1]
    path = Path(*parts).joinpath(number).with_suffix(extension)

    return path


def initiate_status_db(db: str = "status.db"):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    cur.execute("CREATE TABLE records (identifier, status, last_check, last_extraction, last_transformation, last_load);")
    con.commit()
    con.close()


def print_status_db(db: str = "status.db"):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    cur.execute('SELECT COUNT(identifier) FROM records WHERE status="c"')
    print ("checked:     " + str(cur.fetchone()[0]) )
    cur.execute('SELECT COUNT(identifier) FROM records WHERE status="e"')
    print ("extracted:   " + str(cur.fetchone()[0]) )
    cur.execute('SELECT COUNT(identifier) FROM records WHERE status="t"')
    print ("transformed: " + str(cur.fetchone()[0]) )
    cur.execute('SELECT COUNT(identifier) FROM records WHERE status="l"')
    print ("loaded:      " + str(cur.fetchone()[0]) )
    con.close()
    print('----')


def set_status_db(status1: str, status2: str):
    # Changes status1 into status2
    con = sqlite3.connect("status.db")
    cur = con.cursor()
    tupel = (status2, status1)
    cur.execute('UPDATE records SET status = ? WHERE status = ?', tupel)
    con.commit()
    print('status ' + status1 + ' set into ' + status2)
    con.close()


def update_status_db(status: str, db: str = "status.db"):
    # TBD: use pathlib?
    con = sqlite3.connect(db)
    cur = con.cursor()
    if status == 'c':
        now = str(datetime.now())
        record = (now,)
        cur.execute('UPDATE records SET last_check = ?;', record)
        con.commit()
        print('status updated ' + str(record))
    elif status == 'e':
        path = 'extracted'
        for root, subdirs, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(root, filename)
                identifier = filename.split('.')[0]
                mtime = os.path.getmtime(file_path)
                timestamp = datetime.fromtimestamp(mtime).isoformat()
                record = (status, timestamp, identifier)
                cur.execute('UPDATE records SET status = ?, last_extraction = ? WHERE identifier = ?', record)
                con.commit()
                print('status updated ' + str(record))
    elif status == 't':
        path = 'transformed'
        for root, subdirs, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(root, filename)
                identifier = filename.split('.')[0]
                mtime = os.path.getmtime(file_path)
                timestamp = datetime.fromtimestamp(mtime).isoformat()
                record = (status, timestamp, identifier)
                cur.execute('UPDATE records SET status = ?, last_transformation = ? WHERE identifier = ?', record)
                con.commit()
                print('status updated ' + str(record))
    else:
        print('Error in function "update_status_db": Wrong statuscode: ' + status)

    con.close()


def get_process_list_from_status_db(status: str, db: str = "status.db"):
    # Get process_list of identifiers to be processed
    process_list = []
    con = sqlite3.connect(db)
    cur = con.cursor()
    for row in cur.execute('SELECT identifier FROM records WHERE status=?', status):
        process_list.append(row[0])
    con.close()
    print("process_list initiated. " + str(len(process_list)) + " items to be processed.")

    return process_list