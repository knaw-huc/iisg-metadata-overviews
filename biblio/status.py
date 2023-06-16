#!/usr/bin/python3

import sqlite3

con = sqlite3.connect("status.db") 
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