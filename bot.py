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

        Code adapted from https://gist.github.com/yanofsky/5436496
    """

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


def binary_search_tweets_by_date(tweets, targetDate, start, end):
    """ Version of binary search the searches a list tweets and returns the
    index of the tweet with datetime closest to targetDate. If no tweet has
     the same datetime, then it returns the index of the tweet with the closest
     datetime that is less than targetDate.

     Inputs:
        list of status objs. -- tweets -- list of status objects to search
        datetime -- targetDate -- datetime to match
        int -- start -- lower bound of current search area in tweets
        int -- end -- upper bound of current search area in tweets
    Returns:
        int - index of closest tweet that is at or before datetime
    """
    # no exact match in tweets
    if (start > end):
        # TODO will this cover edge cases?? (end and beginning of list?)
        return start - 1

    middle = (start + end) / 2
    value = tweets[middle].created_at

    if value < targetDate:
        return binarySearchTweetsByDate(tweets, targetDate, middle+1, end)
    if value > targetDate:
        return binarySearchTweetsByDate(tweets, targetDate, start, middle-1)
    # found exact match
    return middle


def get_n_neighbors(values, index, n):
    """ Returns a list of the n closest objects in values to index.

        Inputs:
            list -- values -- list to get neighbors from
            int -- index -- index to source neighbors around
            int -- n -- (even) number of neighbors to return
        Returns:
            list -- list of n closest neighbors to index in values
    """
    neighbors = []
    diff = 0
    # check that n/2 lower neighbors exist
    if index >= (n/2):
        for i in range(n/2):
            neighbors.append(values[index - i])
    # add as many as possible, add extra from end if possible
    else:
        diff = (n/2) - index
        for i in range((n/2) - diff):
            neighbors.append(values[index - i])
    # check that n/2 + diff upper neighbors exist, add them
    if len(values) > (index + n/2 + diff):
        for i in range(n/2 + diff):
            neighbors.append(values[index - i])
    # not enough stuff, add as many as possible
    else:
        diffUpp = (len(values) - 1) - index
        for i in range(diffUpp):
            neighbors.append(values[index + i])
    return neighbors


def group_by_date(sourceTweets):
    """ Returns a dictionary grouping user tweets with associated context.
        Context of a tweet is 5 closest tweets (by time) from each news source
        (25 total tweets).

        Inputs:
            list of lists of status objects -- sourceTweets -- list of all
                tweets from user and contexts [[all users], [all source 1],...]
        Returns:
            dictionary (tweetid, list of status objs.) -- dictionary of contexts
                for each user tweet, keyed by unique ids
    """
    # init diction of context for each tweet
    contextByTweet = {}
    # get list of user tweets
    userTweets = sourceTweets[0]

    # get all context tweets
    contextTweets = sourceTweets[1:]

    for status in userTweets:
        tweetId = status.id  # int
        tweetDatetime = status.created_at  # datetime obj
        context = []
        # find five closest tweets form each context (by time)
        for source in contextTweets:
            # get context tweet closest (at or before) status
            closest = binary_search_tweets_by_date(source, tweetDatetime, 0, len(source - 1))
            # get 4 neighbors (2 before and 2 after if possible, or closest)
            neighbors = get_four_neighbors(source, closest, 4)
            # build context
            context = neighbors.append(closest)
        # add context with tweet to dict
        contextByTweet[tweetId] = context

    return contextByTweet


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
