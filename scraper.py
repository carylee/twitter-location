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

MAX_QUERIES = 200/2
# Use this for testing
#MAX_QUERIES = 5/2
MAX_TWEETS = 190
DB = 'tweets.db'

                 
############################
#     Helper Functions     #
############################  

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

def printTweetsInfo(tweets, numFailed):
    # I am assuming at some point we will want a fancier print function
    print 'Number of Tweets added ', (len(tweets) - numFailed)

def printUsersInfo(users, numFailed):
    # I am assuming at some point we will want a fancier print function
    print 'Number of Valid Users added ', (len(users) - numFailed)

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
              
def printDatabaseInfo(cursor):
    cursor.execute('select count(*) from users')
    numUsers = cursor.fetchall()
    cursor.execute('select count(*) from status')
    numTweets = cursor.fetchall()
    print "There are currently %d users and %d tweets in the database.\n" % (numUsers[0][0], numTweets[0][0])






#######################
#     Grab Tweets     #
#######################

localtime = time.localtime(time.time())
initTweets = api.GetPublicTimeline()
users = filterUsers( getUsers( filterUsers([s.user for s in initTweets])))
tweets = getTweets(users)



#############################
#     Put into Database     #
#############################

connection = sqlite.connect(DB)
cursor = connection.cursor()
userInsertFail = 0
tweetInsertFail = 0

for user in users:
    values = formatUser(user)
    try:
        cursor.execute('insert into users values (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
        connection.commit()
    except:
        userInsertFail += 1
        continue

for tweet in tweets:
    values = formatTweet(tweet)
    try:
        cursor.execute('insert into status values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
        connection.commit()
    except:
        tweetInsertFail += 1
        continue


#########################
#     Print Summary     #
#########################

print "Ran at: %s:%s on %s/%s/%s" % (localtime.tm_hour, localtime.tm_min, localtime.tm_mon, localtime.tm_mday, localtime.tm_year)
printUsersInfo(users, userInsertFail)
printTweetsInfo(tweets, tweetInsertFail)
printDatabaseInfo(cursor)
cursor.close()



