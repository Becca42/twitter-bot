# twitter-bot
Twitter bot for 4701
(API Page: https://apps.twitter.com/app/13003546/keys)

CODING HELP FROM:
http://blog.mollywhite.net/twitter-bots-pt2/#createthetwitterapp :: (How to create a Twitter bot)
https://gist.github.com/yanofsky/5436496 :: (Pulling Twitter Data)
http://tweepy.readthedocs.io/en/v3.5.0/api.html#timeline-methods :: (Tweepy Documentation)
http://tkang.blogspot.com/2011/01/tweepy-twitter-api-status-object.html :: (Tweepy Status Object Description)
http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python :: (URL Regex Pattern)

CONCEPTUAL HELP FROM:
http://colah.github.io/posts/2015-08-Understanding-LSTMs/ :: (Understanding LSTM Networks)
https://www.youtube.com/watch?v=hWgGJeAvLws :: (TensorFlow RNN mini-tutorial)
https://arxiv.org/pdf/1409.2329.pdf :: (Recurrent Neural Network Regularization)
http://karpathy.github.io/2015/05/21/rnn-effectiveness/ :: (The Unreasonable Effectiveness of Recurrent Neural Networks)
http://lauragelston.ghost.io/speakeasy-pt2/ :: (BUILDING A CHATBOT, PT. 2: BUILDING A CONVERSATIONAL TENSORFLOW MODEL)
http://suriyadeepan.github.io/2016-06-28-easy-seq2seq/ :: (Chatbots with Seq2Seq)

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
	TODO 3.d -- remove URLs -- Done
	TODO 3.e -- remove &amp etc. -- 
	TODO 3.f -- partition off a test set -- Done?
TODO 4 -- adapt data_utils for this project -- Done 
TODO 5 -- set up neural net -- In Progress
	TODO 4.a -- import tensorflow -- Done
	TODO 4.b -- update graph to work for my input -- In Progress
TODO 6 -- train and test -- 