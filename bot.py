from secrets import *
import tweepy
import threading

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
# Construct the API instance
api = tweepy.API(auth)


def get_all_tweets(user, alltweets):
    """ Modifies alltweets to contain all tweets posted by user with screen-name "user"

        Input:
            string -- user -- user name of a given twitter account
        Returns:
            list of Status objects -- all tweets of user (max 3240)

        Code adapted from https://gist.github.com/yanofsky/5436496 """

    #TODO check that user is a valid screen name??

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


def date_posted(tweet):
    """ Returns the date that status object tweet was created

        Inputs:
            status obj. -- tweet -- a tweet rep. as a status obj.
        Returns:
            datetime.date -- the date the tweet was created (posted)
    """
    return tweet.created_at.date()


def group_by_date(sourceTweets):
    """ Returns a dictionary grouping user tweets with associated context.
        Context of a tweet is 5 closest tweets (by time) from each news source
        (25 total tweets).

        Inputs:
            sourceTweets -- list of lists of status objects -- list of all
                tweets from user and contexts [[all users], [all source 1],...]
        Returns:
            dictionary (tweetid, list of tweet ids) -- dictionary of contexts
                for each user tweet, stored by unique ids
    """
    # TODO implement this function


if __name__ == '__main__':
    user = 14294848  # @snopes
    news1 = 807095  # @nytimes
    news2 = 1367531  # @FoxNews
    news3 = 1652541  # @Reuters
    news4 = 457984599  # @BreitbartNews
    news5 = 2467791  # @washingtonpost

    # grab all tweets from user
    userHistory = []
    tu = threading.Thread(target=get_all_tweets, args=(user, userHistory))
    # get all tweets from context users
    news1History = []
    t1 = threading.Thread(target=get_all_tweets, args=(news1, news1History))
    news2History = []
    t2 = threading.Thread(target=get_all_tweets, args=(news2, news2History))
    news3History = []
    t3 = threading.Thread(target=get_all_tweets, args=(news3, news3History))
    news4History = []
    t4 = threading.Thread(target=get_all_tweets, args=(news4, news4History))
    news5History = []
    t5 = threading.Thread(target=get_all_tweets, args=(news5, news5History))

    # run threads
    tu.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    tu.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
