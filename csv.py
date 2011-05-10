#! /usr/bin/python
from pysqlite2 import dbapi2 as sqlite
import sys

DB = 'tweets.db'
#DB = 'test.db'

con = sqlite.connect(DB)
cur = con.cursor()

cur.execute('select place_id, text from status where place_id is not "\'None\'"')
tw = cur.fetchall()
print 'ghj;'
f = open('test.csv', 'w')

f.write("place,tweet\n")

for tweets in tw:
    s = tweets[0].rfind('full_name') + 14
    e = tweets[0].rfind('attributes') - 5
    if e < 0:
        print 'oh shit!'
    else:
        loc = tweets[0][s:e]
        loc = loc.replace( ', ', '#')
        t = tweets[1][2:-2]
        t = t.replace(',', '')
        u = unicode(loc + ',' + t + '\n')
        f.write(u.encode('ascii', 'replace'))

f.close()





