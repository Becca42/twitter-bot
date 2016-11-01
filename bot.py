from secrets import *
import tweepy

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
# Construct the API instance
api = tweepy.API(auth)


def get_all_tweets(user):
    """ Returns list of all tweets posted by user with screen-name "user"

        Input:
            string -- user -- user name of a given twitter account
        Returns:
            list of Status objects -- all tweets of user (max 3240)

        Code adapted from https://gist.github.com/yanofsky/5436496 """

    #TODO check that user is a valid screen name??

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(user, 200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        #all subsiquent requests starting with oldest
        new_tweets = api.user_timeline(user, 200, oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    return alltweets
