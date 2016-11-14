# twitter-bot
Twitter bot for 4701
(API Page: https://apps.twitter.com/app/13003546/keys)

HELP FROM:
http://blog.mollywhite.net/twitter-bots-pt2/#createthetwitterapp :: (How to create a Twitter bot)
https://gist.github.com/yanofsky/5436496 :: (Pulling Twitter Data)
http://tweepy.readthedocs.io/en/v3.5.0/api.html#timeline-methods :: (Tweepy Documentation)
http://tkang.blogspot.com/2011/01/tweepy-twitter-api-status-object.html :: (Tweepy Status Object Description)

INSPIRATION FROM:
https://chatbotsmagazine.com/the-guide-to-designing-a-magical-chatbot-experience-part-1-efbf32444448#.c0zwiv4e3 :: (The Guide To Designing A Magical Chatbot Experience — Part 1)

TODO LIST:
TODO 1 -- set up twitter account -- Done
TODO 2 -- gather user data -- Done
	TODO 2.a -- find API tool to collect data -- Done (Tweepy)
	TODO 2.b -- pick a user -- Done (Snopes.com)
TODO 3 -- split into training and test set --
	TODO 3.a decide what to test on (e.g. snopes + trending hashtags, snopes + 5-10 other news sources) -- Done (other news twitters)
	TODO 3.b -- get data from "environment" users -- Done (nytimes, foxnews, reuters, breitbart, wapo)
	TODO 3.b.i -- parallelize requests to speed up process -- Done
	TODO 3.c -- partition by date -- Done
TODO 4 -- set up neural net -- In Progress?
	TODO 4.a -- 
TODO 5 -- 