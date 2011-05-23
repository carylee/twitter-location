import sqlite3, re, csv, json
#import codecs, cStringIO

#db = 'tweets.db'
db = 'test.db'

con = sqlite3.connect(db)
cur = con.cursor()

cur.execute('select id,user_id,place_id,text from status where place_id!="\'None\'"')
tweets = cur.fetchall()


def makeInsert(tweetId, text, user, placeName, placeFullName, country, placeId):
  location = user['location'] if 'location' in user else ''
  userName = user['name'] if 'name' in user else ''
  screenName = user['screen_name'] if 'screen_name' in user else ''
  utc = str(user['utc_offset']) if 'utc_offset' in user else ''
  timezone = user['time_zone'] if 'time_zone' in user else ''
  description = user['description'] if 'description' in user else ''
  description = re.sub("['\"]", '', description)
  lang = user['lang'] if 'lang' in user else ''
  return "INSERT INTO tweets \
(id,user_lang,user_loc,user_name,screen_name,utc_offset,time_zone,user_description,text,place_name,place_full_name,country,place_id) \
VALUES ('" + str(tweetId) + "', '" + lang + "','" + location + "', '" + userName + "', '" + screenName + "', \
'" + utc + "','" + timezone + "','" + description + "','" + text + "','" + placeName + "','" + placeFullName + "','" + country + "','" + placeId + "');"


for tweet in tweets:
  user = json.loads(tweet[1])
  text = re.sub('\n', ' ', tweet[3])
  text = re.sub("\s?'$", ' ', text)
  text = re.sub("^'\s?", ' ', text)
  text = re.sub("\"|'", '', text)
  place = tweet[2]
  placeNameMatches = re.search("(?<='name': u)['\"](.*?)[\"'],", place)
  placeName = str(placeNameMatches.group(1)) if placeNameMatches else ''
  placeFullNameMatches = re.search("(?<='full_name': u)['\"](.*?)[\"'],", place)
  placeFullName = str(placeFullNameMatches.group(1)) if placeFullNameMatches else ''
  countryMatches = re.search("(?<='country': u)['\"](.*?)[\"'],", place)
  country = str(countryMatches.group(1)) if countryMatches else ''
  placeIdMatches = re.search("(?<='id': u)['\"](.*?)['\"}]", place)
  placeId = str(placeIdMatches.group(1)) if placeIdMatches else ''
  insert = makeInsert(tweet[0],text,user,placeName,placeFullName,country,placeId)
  print insert.encode('ascii', 'ignore')
