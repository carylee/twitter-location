import sqlite3, re, csv
import codecs, cStringIO

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

#db = 'tweets.db'
db = 'test.db'

con = sqlite3.connect(db)
cur = con.cursor()

cur.execute('select place_id, text from status where place_id!="\'None\'"')
tweets = cur.fetchall()

writer = UnicodeWriter(open('tweets.csv', 'wb'), quoting=csv.QUOTE_ALL, quotechar="'")

writer.writerow(['text', 'place_name', 'place_full_name', 'place_country'])

#fulltweets = []

for tweet in tweets:
  text = re.sub('\n', ' ', tweet[1])
  text = re.sub("\s?'$", ' ', text)
  text = re.sub("^'\s?", ' ', text)
  text = re.sub("\"|'", '', text)
  place = tweet[0]
  placeNameMatches = re.search("(?<='name': u)['\"](.*?)[\"'],", place)
  placeName = str(placeNameMatches.group(1))
  placeFullNameMatches = re.search("(?<='full_name': u)['\"](.*?)[\"'],", place)
  placeFullName = str(placeFullNameMatches.group(1))
  countryMatches = re.search("(?<='country': u)['\"](.*?)[\"'],", place)
  country = str(countryMatches.group(1))
  writer.writerow([text, placeName, placeFullName, country])

#writer.writerows(fulltweets)


