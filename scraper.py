import twitter
from config import Config

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
print api.VerifyCredentials() 
                  
############################
#     Helper Functions     #
############################  

#MAX_QUERIES = 349/2
# Use this for testing
MAX_QUERIES = 50/2
MAX_TWEETS = 190


def getUsers(users):
    i = 0
    print len(users)
    while len(users) < MAX_QUERIES:
        user = users[i]
        print 'here ' + str(i) 
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

################
#     Main     #
################  


initTweets = api.GetPublicTimeline()
#users = getUsers([s.user for s in initTweets])

tweets = getTweets( filterUsers( getUsers( filterUsers([s.user for s in initTweets]))))

# Write some LEET shiet to load into the database
print len(tweets)
for u, t in tweets.iteritems():
    if len(t) > 0:
        print 'number of tweets: %s; 1st tweet: %s' % (len(t), t[0].text)
    else:
        print 'null tweet'
    



        
        
