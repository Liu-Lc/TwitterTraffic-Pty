#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Starts the streaming of tweets following the keywords:
@traficocpanama, traficocpanama, trafico panama.
See Listener on_status function to see processes done when 
a new tweet is streamed.

Created on Sun Apr 18 17:44 2021
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

from tweepy import API, OAuthHandler, Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError
from keys import *

class SListener(StreamListener):

    # initialize API
    def __init__(self, api=None, fprefix='streamer'):
        self.api = api or API()
        # set db connection
        # self.db = DB_Connection()

    # for each tweet streamed
    def on_status(self, status):
        # parse status object into JSON
        # status_json = json.dumps(status._json)
        # # convert json string to dictionary
        # status_data = json.loads(status_json)

        # If tweet is not a retweet and tweet is in English
        if not hasattr(status, "retweeted_status"):
            tweet_id = status.id
            user_id = status.user.screen_name
            user_name = status.user.name
            tweet_created = status.created_at

            # Tweet
            if status.truncated == True:
                text = status.extended_tweet['full_text']
            else:
                text = status.text
            
            # link
            link = 'https://www.twitter.com/' + str(user_id) + '/status/' + str(tweet_id)

            # Connect to database
            print([tweet_id, tweet_created, user_id, user_name, link])
            print(text)
            print('\n')

    # if theres an error
    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False

# consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)
# access key authentication
auth.set_access_token(access_token, access_token_secret)
# set up API with authentication handler
api = API(auth, wait_on_rate_limit=True)

# instantiate the SListener object
listen = SListener(api)
# instantiate the stream object
stream = Stream(auth, listen)

# set keywords
keywords = ['@traficocpanama,traficocpanama,trafico panama']
# keywords = ['accidente']

# begin collecting data
while True:
    # maintian connection unless interrupted
    try:
        stream.filter(track=keywords)
    # reconnect automantically if error arise
    # due to unstable network connection
    except (ProtocolError, AttributeError):
        continue