#!/usr/bin/env python

import sqlite3
from numpy import loadtxt, zeros_like, c_
import numpy as np
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
for i,cname in enumerate(cnames):
    print i, cname

cnames[0] = 'zz'
cnames[1] = 'lage'
cnames[4] = 'logL'
cnames[8] = 'u'
cnames[9] = 'g'
cnames[10] = 'r'
cnames[11] = 'i'
cnames[12] = 'z'
cnames[13] = 'Y'

sql_query = 'CREATE TABLE padova_des ( Z_met float, '
ncols = "( ?, "

for cname in cnames:
    sql_query += unicode(cname)
    if cname != cnames[-1]:
        sql_query += ' float, '
        ncols += ' ?, '
    else:
        # primary key as age and met
        sql_query += ' float )'
        ncols += ' ? )'

mydb = 'isoc.sqlite'
conn = sqlite3.connect(mydb)
cursor = conn.cursor()
cursor.execute(sql_query)

Zlist = np.array([])
agelist = np.loadtxt(argv[1], usecols=(1,))
agelist = np.unique(agelist)

for fname in argv[1:]: 
    a = open(fname, 'r')
    line = a.readline()
    while '#' in line:
        if 'Isochrone' in line:
            Z = line.split()[4]
            Zlist = np.r_[Zlist, float(Z)]
            line = " "
        else:
            line = a.readline()
    a.close()

    f = loadtxt(fname)
    b = zeros_like(f[:,0])
    b += float(Z)
    f = c_[b, f]
    cursor.executemany('insert into padova_des values ' + ncols, f[:,])

cursor.execute('CREATE TABLE age_grid (lage float)')
for AGE in agelist:
    print AGE
    cursor.execute('INSERT INTO age_grid values (?) ', [AGE])

cursor.execute('CREATE TABLE met_grid (Z_met float)')
for MET in Zlist:
    cursor.execute('INSERT INTO met_grid values (?) ', [MET])


conn.commit()
cursor.close()
