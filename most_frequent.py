#!/usr/bin/python
import re, csv, sys
import codecs, cStringIO
import MySQLdb as db




class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def most_common(lst):
    return max(set(lst), key=lst.count)

conn = db.connect('localhost', 'daniel', 'glhh2o', 'tweets');
cur = conn.cursor()

cur.execute('select concat(text), screen_name from tweets group by screen_name')
tweets = cur.fetchall()

blacklist = []

writer = UnicodeWriter(open('most_frequent.csv', 'wb'), quoting=csv.QUOTE_ALL, quotechar="'")

writer.writerow(['text', 'place_name', 'place_full_name', 'place_country', 'screen_name'])

for tweet in tweets:
    user = tweet[1]
    if user not in blacklist:
        cur.execute('select place_full_name from tweets where screen_name = %s', user)
        fullPlaceName = cur.fetchall()
        mostCommon =  most_common(fullPlaceName)[0]
        cur.execute('select place_name, place_full_name, country from tweets where screen_name = %s and place_full_name = %s', (user, mostCommon))
        placeInfo = cur.fetchone()
        blacklist.append(user)
        writer.writerow([tweet[0], placeInfo[0], placeInfo[1], placeInfo[2], user])

conn.close()


