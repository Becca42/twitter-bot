"""Utilities for downloading data from WMT, tokenizing, vocabularies."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os
import re
import tarfile

from six.moves import urllib

from tensorflow.python.platform import gfile
#################

from secrets import *
import tweepy
import threading
import re  # regex library

# Special vocabulary symbols - we always put them at the start.
_PAD = b"_PAD"
_GO = b"_GO"
_EOS = b"_EOS"
_UNK = b"_UNK"
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile(b"([.,!?\"':;)(])")
_DIGIT_RE = re.compile(br"\d")
#################
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
# Construct the API instance
api = tweepy.API(auth)

#############################################################
# functions adapted from tensorflow example file data_utils #
#############################################################

# TODO call this on all tweets
def basic_tokenizer(sentence):
  """Very basic tokenizer: split the sentence into a list of tokens."""
  words = []
  for space_separated_fragment in sentence.strip().split():
    words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
  return [w for w in words if w]


def create_vocabulary(vocabulary_path, data_path, max_vocabulary_size,
                      tokenizer=None, normalize_digits=True):
    """Create vocabulary file (if it does not exist yet) from data file.

    Data file is assumed to contain one sentence per line. Each sentence is
    tokenized and digits are normalized (if normalize_digits is set).
    Vocabulary contains the most-frequent tokens up to max_vocabulary_size.
    We write it to vocabulary_path in a one-token-per-line format, so that later
    token in the first line gets id=0, second line gets id=1, and so on.

    Args:
    vocabulary_path: path where the vocabulary will be created.
    data_path: data file that will be used to create vocabulary.
    max_vocabulary_size: limit on the size of the created vocabulary.
    tokenizer: a function to use to tokenize each data sentence;
      if None, basic_tokenizer will be used.
    normalize_digits: Boolean; if true, all digits are replaced by 0s.
    """
    if not gfile.Exists(vocabulary_path):
        print("Creating vocabulary %s from data %s" % (vocabulary_path, data_path))
        vocab = {}
        with gfile.GFile(data_path, mode="rb") as f:
            counter = 0
        for line in f:
            counter += 1
            if counter % 100000 == 0:
                print("  processing line %d" % counter)
            tokens = tokenizer(line) if tokenizer else basic_tokenizer(line)
            for w in tokens:
                word = re.sub(_DIGIT_RE, b"0", w) if normalize_digits else w
                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1
        vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
        if len(vocab_list) > max_vocabulary_size:
            vocab_list = vocab_list[:max_vocabulary_size]
        with gfile.GFile(vocabulary_path, mode="wb") as vocab_file:
            for w in vocab_list:
                vocab_file.write(w + b"\n")


def initialize_vocabulary(vocabulary_path):
    """Initialize vocabulary from file.

    We assume the vocabulary is stored one-item-per-line, so a file:
    dog
    cat
    will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
    also return the reversed-vocabulary ["dog", "cat"].

    Args:
    vocabulary_path: path to the file containing the vocabulary.

    Returns:
    a pair: the vocabulary (a dictionary mapping string to integers), and
    the reversed vocabulary (a list, which reverses the vocabulary mapping).

    Raises:
    ValueError: if the provided vocabulary_path does not exist.
    """
    if gfile.Exists(vocabulary_path):
        rev_vocab = []
        with gfile.GFile(vocabulary_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
        rev_vocab = [line.strip() for line in rev_vocab]
        vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_path)


def sentence_to_token_ids(sentence, vocabulary,
                          tokenizer=None, normalize_digits=True):
    """Convert a string to list of integers representing token-ids.

    For example, a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].

    Args:
    sentence: the sentence in bytes format to convert to token-ids.
    vocabulary: a dictionary mapping tokens to integers.
    tokenizer: a function to use to tokenize each sentence;
      if None, basic_tokenizer will be used.
    normalize_digits: Boolean; if true, all digits are replaced by 0s.

    Returns:
    a list of integers, the token-ids for the sentence.
    """
    if tokenizer:
        words = tokenizer(sentence)
    else:
        words = basic_tokenizer(sentence)
    if not normalize_digits:
        return [vocabulary.get(w, UNK_ID) for w in words]
    # Normalize digits by 0 before looking words up in the vocabulary.
    return [vocabulary.get(re.sub(_DIGIT_RE, b"0", w), UNK_ID) for w in words]

#####################################################


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


def cleanse_urls(tweets):
    """ identify and replace urls in tweets

        Inputs:
            list of strings -- tweets -- list of tweets
        Returns:
            list of strings -- tweets with urls replaced with "URL"
    """
    cleansed = []
    # set up url regex
    # regex pattern from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
    regURL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # for each tweet object find and replace any urls
    for tweet in tweets:
        # split tweet into list
        tList = tweet.text.split()
        for i in range(len(tList)):
            match = regURL.match(tList[i])
            if match:
                tList[i] = "URL"
        # rejoin updated list into string, add to cleansed list
        tweet.text = ' '.join(tList)
        cleansed.append(tweet)
    return cleansed


def download_and_prepare():
    """Get tweet data into data_dir (TODO??????), create vocabularies and tokenize data.

    Inputs:
        none

    Returns:
    A tuple of 6 elements:
      (1) path to the token-ids for English training data-set,
      (2) path to the token-ids for French training data-set,
      (3) path to the token-ids for English development data-set,
      (4) path to the token-ids for French development data-set,
      (5) path to the English vocabulary file,
      (6) path to the French vocabulary file.
    """
    # set source twitter IDS
    user = 14294848  # @snopes
    news1 = 807095  # @nytimes
    news2 = 1367531  # @FoxNews
    news3 = 1652541  # @Reuters
    news4 = 759251  # @CNN
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
    threads = [tu, t1, t2, t3, t4, t5]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    # clean urls of all tweets
    allTweets = [userHistory, news1History, news2History, news3History, news4History, news5History]
    for i in range(len(allTweets)):
        allTweets[i] = cleanse_urls(allTweets[i])

    ##################################################################
    # following code adapted from tensorflow example file data_utils #
    ##################################################################

    # TODO build vocab

    # set paths for storing data
    data_dir = "tweet_data"
    train_dir = "tweet_train"
    train_path = os.path.join(data_dir, "context")
    dev_path = os.path.join(data_dir, "test1")
     # set vocab size
    vocab_size = 500000  # TODO update if necessary

    user_path = os.path.join(data_dir, "vocab%d.user" % vocab_size)
    context_path = os.path.join(data_dir, "vocab%d.context" % vocab_size)
    create_vocabulary(context_path, train_path + ".context", vocab_size, None)  # None: user default tokenizer
    create_vocabulary(user_path, train_path + ".user", vocab_size, None)

    # TOOD tokenize
    # Create token ids for the training data.
    user_train_ids_path = train_path + (".ids%d.user" % vocab_size)
    context_train_ids_path = train_path + (".ids%d.context" % vocab_size)
    data_to_token_ids(train_path + ".user", user_train_ids_path, user_path, None)
    data_to_token_ids(train_path + ".en", en_train_ids_path, en_vocab_path, None)

    print("made it")

    # Create token ids for the development data.
    user_dev_ids_path = dev_path + (".ids%d.user" % vocab_size)
    context_dev_ids_path = dev_path + (".ids%d.context" % vocab_size)
    data_to_token_ids(dev_path + ".fr", user_dev_ids_path, user_path, None)
    data_to_token_ids(dev_path + ".en", context_dev_ids_path, context_path, None)

    # TODO return paths to directories of input and output
    return (user_train_ids_path, context_train_ids_path,
          context_dev_ids_path, user_dev_ids_path,
          context_path, user_path)
