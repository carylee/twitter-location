import twitter
from config import Config

############################
#     Helper Functions     #
############################  

f = file('myconfig.cfg')
cfg = Config(f)
api = twitter.Api(consumer_key = cfg.oAuth[0].consumer_key, 
                  consumer_secret = cfg.oAuth[0].consumer_key,
                  access_token_key = cfg.oAuth[0].consumer_key,
                  access_token_secret= cfg.oAuth[0].consumer_key)
                  
############################
#     Helper Functions     #
############################  

def getUsers(users):
    for user in users:
        if len(users) < MAX_QUERIES:
            users += api.GetFriends(user = user)
        else:
            return users

    return users

def getTweets(users):
    tweets = {}
    for user in users:
        tweets[str(user)] = api.GetUserTimeline(user, count = MAX_TWEETS)
    return tweets

################
#     Main     #
################  

#MAX_QUERIES = 349/2
# Use this for sexting
MAX_QUERIES = 10/2
MAX_TWEETS = 200


initTweets = api.GetPublicTimeline()
users = getUsers([s.user.id for s in initTweets])
tweets = getTweets(users)
# Write some LEET shiet to load into the database
for u, t in tweets.iteritems():
    print t[0].text
    



        
        
