#! /usr/bin/python

import twitter
from config import Config
from pysqlite2 import dbapi2 as sqlite


############################
#       Configuration      #
############################  
if 
f = file('myconfig.cfg')
cfg = Config(f)
api = twitter.Api(consumer_key = cfg.oAuth[0].consumer_key, 
                  consumer_secret = cfg.oAuth[0].consumer_secret,
                  access_token_key = cfg.oAuth[0].access_token,
                  access_token_secret= cfg.oAuth[0].access_token_secret)

#just checking that I logged in...
#print api.VerifyCredentials() 
                  
############################
#     Helper Functions     #
############################  

#MAX_QUERIES = 349/2
# Use this for testing
MAX_QUERIES = 20/2
MAX_TWEETS = 190
DB = 'tweets.db'

def getUsers(users):
    i = 0
    print 'grabbed %s legit users' % (str(len(users)))
    while len(users) < MAX_QUERIES:
        user = users[i]
        i += 1
        # only grab first 10 friends
        users.extend( api.GetFriends(user = user.id)[:10] )
    return users

def filterUsers(users):
    for user in users[:]:
        if user.GetLang() != 'en':
            users.remove(user)
        elif user.GetProtected():
            users.remove(user)
    return users

def getTweets(users):
    tweets = {}
    for user in users:
        if user.GetProtected():
            print 'oh no !'
        try:
            tweets[str(user.id)] = api.GetUserTimeline(user.id, count = MAX_TWEETS)
        except:
            continue
    return tweets

#######################
#     Grab Tweets     #
#######################

initTweets = api.GetPublicTimeline()
#users = getUsers([s.user for s in initTweets])
users = filterUsers( getUsers( filterUsers([s.user for s in initTweets]))) 
tweets = getTweets(users)

print len(tweets)
for u, t in tweets.iteritems():
    if len(t) > 0:
        print 'number of tweets: %s; 1st tweet: %s' % (len(t), t[0].text)
    else:
        print 'null tweet'
    
#############################
#     Put into Database     #
#############################

connection = sqlite.connect(DB)
cursor = connection.cursor()

for user in users:
    if user.GetGeoEnabled():
        values = (unicode(user.GetId()),
                  '\'' + unicode(user.GetName()) + '\'',
                  '\'' + unicode(user.GetCreatedAt()) + '\'', 
                  '\'' + unicode(user.GetLocation()) + '\'', 
                  '\'' + unicode(user.GetDescription()) + '\'', 
                  unicode(1),
                  unicode(user.GetFriendsCount()),
                  unicode(user.GetStatusesCount()), 
                  '\'' + unicode(user.GetScreenName()) + '\'',
                  '\'' + unicode(user.GetTimeZone()) + '\'', 
                  '\'' + unicode(user.GetUrl()) + '\'',
                  unicode(user.GetUtcOffset()), 
                  '\'' + unicode(user.GetLang()) + '\'')
    else:
        values = (unicode(user.GetId()),
                  '\'' + unicode(user.GetName()) + '\'',
                  '\'' + unicode(user.GetCreatedAt()) + '\'', 
                  '\'' + unicode(user.GetLocation()) + '\'', 
                  '\'' + unicode(user.GetDescription()) + '\'', 
                  unicode(0),
                  unicode(user.GetFriendsCount()),
                  unicode(user.GetStatusesCount()), 
                  '\'' + unicode(user.GetScreenName()) + '\'',
                  '\'' + unicode(user.GetTimeZone()) + '\'', 
                  '\'' + unicode(user.GetUrl()) + '\'',
                  unicode(user.GetUtcOffset()), 
                  '\'' + unicode(user.GetLang()) + '\'')
    cursor.execute('insert into users values (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
    connection.commit()
#for tweet in tweets:
#    cursor.execute('insert into status values ()')

#connection.commit()



#  id integer primary key,
#  name text,
#  created_at text,
#  location text,
#  description text,
#  geo_enabled tinyint(1),
#  friends_count integer,
#  statuses_count integer,
#  screen_name text,
#  time_zone text,
#  url text,
#  utc_offset integer,
#  lang en
