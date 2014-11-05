#!/usr/bin/env python

import sqlite3
from numpy import loadtxt, zeros_like, c_
from sys import argv


a = open(argv[1], 'r')
line = a.readline()

while '#' in line:
    if 'Isochrone' in line:
        Z = line.split()[4]
        cnames= a.readline().split()[1:]
        line = " "
    else:
        line = a.readline()
a.close()

#bad columns
cnames[0] = 'lage'
cnames[3] = 'logL'
cnames[15] = 'CO'

sql_query = 'CREATE TABLE padova_sdss ( Z_met float, '
ncols = "( ?, "

for cname in cnames:
    sql_query += unicode(cname)
    if cname != cnames[-1]:
        sql_query += ' float, '
        ncols += ' ?, '
    else:
        sql_query += ' float )'
        ncols += ' ? )'

mydb = 'isoc.sqlite'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()
cursor.execute(sql_query)

for fname in argv[1:]: 
    a = open(fname, 'r')
    line = a.readline()
    while '#' in line:
        if 'Isochrone' in line:
            Z = line.split()[4]
            line = " "
        else:
            line = a.readline()
    a.close()

    f = loadtxt(fname)
    b = zeros_like(f[:,0])
    b += float(Z)
    f = c_[b, f]
    cursor.executemany('insert into padova_sdss values ' + ncols, f[:,])

conn.commit()
cursor.close()
