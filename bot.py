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
    new_tweets = api.user_timeline(user, count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)
    print alltweets[0].text

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    print "starting loop"
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        #all subsiquent requests starting with oldest
        new_tweets = api.user_timeline(user, count=200, max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    print alltweets[-1].text
    print len(alltweets)
    return alltweets


if __name__ == '__main__':
    user = 14294848  # @snopes
    news1 = 807095  # @nytimes
    news2 = 1367531  # @FoxNews
    news3 = 1652541  # @Reuters
    news4 = 457984599  # @BreitbartNews
    news5 = 2467791  # @washingtonpost

    # grab all tweets from user
    userHistory = get_all_tweets(user)

    news1History = get_all_tweets(news1)
    news2History = get_all_tweets(news2)
    news3History = get_all_tweets(news3)
    news4History = get_all_tweets(news4)
    news5History = get_all_tweets(news5)
