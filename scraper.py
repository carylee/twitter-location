#! /usr/bin/python

import twitter, time
from config import Config
from pysqlite2 import dbapi2 as sqlite


############################
#       Configuration      #
############################
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

MAX_QUERIES = 300/2
# Use this for testing
#MAX_QUERIES = 5/2
MAX_TWEETS = 190
DB = 'tweets.db'

def getUsers(users):
    i = 0
    while len(users) < MAX_QUERIES:
        user = users[i]
        i += 1
        users.extend( api.GetFriends(user = user.id)[:10] )
    return users

def filterUsers(users):
    for user in users[:]:
        if user.GetLang() != 'en' or user.GetProtected():
            users.remove(user)
    return users

def getTweets(users):
    tweets = []
    for user in users:
        if not user.GetProtected():
            try:
                tweets += api.GetUserTimeline(user.id, count = MAX_TWEETS)
            except:
                continue
    return tweets

def printTweetsInfo(tweets):
    # I am assuming at some point we will want a fancier print function
    print 'Number of Tweets ', len(tweets)

def printUsersInfo(users):
    # I am assuming at some point we will want a fancier print function
    print 'Number of Valid Users', len(users)

def formatUser(user):
    return (unicode(user.GetId()),
              '\'' + unicode(user.GetName()) + '\'',
              '\'' + unicode(user.GetCreatedAt()) + '\'', 
              '\'' + unicode(user.GetLocation()) + '\'', 
              '\'' + unicode(user.GetDescription()) + '\'', 
              unicode(int(user.GetGeoEnabled())),
              unicode(user.GetFriendsCount()),
              unicode(user.GetStatusesCount()), 
              '\'' + unicode(user.GetScreenName()) + '\'',
              '\'' + unicode(user.GetTimeZone()) + '\'', 
              '\'' + unicode(user.GetUrl()) + '\'',
              unicode(user.GetUtcOffset()), 
              '\'' + unicode(user.GetLang()) + '\'')

def formatTweet(tweet):
    return (unicode(tweet.GetId()),
              '\'' + unicode(tweet.GetCreatedAt()) + '\'',
              unicode(tweet.GetUser()),
              unicode(int(tweet.GetFavorited())),
              '\'' + unicode(tweet.GetInReplyToScreenName()) + '\'',
              unicode(tweet.GetInReplyToUserId()),
              unicode(tweet.GetInReplyToStatusId()),
              unicode(int(tweet.GetTruncated())),
              '\'' + unicode(tweet.GetSource()) + '\'',
              '\'' + unicode(tweet.GetText()) + '\'',
              '\'' + unicode(tweet.GetLocation()) + '\'',
              '\'' + unicode(tweet.GetRelativeCreatedAt()) + '\'',
              '\'' + unicode(tweet.GetUser()) + '\'',
              '\'' + unicode(tweet.GetGeo()) + '\'',
              '\'' + unicode(tweet.GetPlace()) + '\'',
              '\'' + unicode(tweet.GetCoordinates()) + '\'')
              

#######################
#     Grab Tweets     #
#######################

# Print some log information
localtime = time.localtime(time.time())
print "\n\nRan at: %s:%s on %s/%s/%s" % (localtime.tm_hour, localtime.tm_min, localtime.tm_mon, localtime.tm_mday, localtime.tm_year)


initTweets = api.GetPublicTimeline()

users = filterUsers( getUsers( filterUsers([s.user for s in initTweets])))
printUsersInfo(users)

tweets = getTweets(users)
printTweetsInfo(tweets)




#############################
#     Put into Database     #
#############################

connection = sqlite.connect(DB)
cursor = connection.cursor()

for user in users:
    values = formatUser(user)
    cursor.execute('insert into users values (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
    connection.commit()

for tweet in tweets:
    values = formatTweet(tweet)
    cursor.execute('insert into status values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
    connection.commit()

print "\n"
