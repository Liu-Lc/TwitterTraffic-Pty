#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Starts the streaming of tweets following the keywords:
@traficocpanama, traficocpanama, trafico panama.
See Listener on_status function to see processes done when 
a new tweet is streamed.

Created on Sun Apr 18 17:44 2021
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import time
from datetime import timedelta

from tweepy import API, OAuthHandler, Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError

import DBConnect
import keys


class SListener(StreamListener):

    # initialize API
    def __init__(self, api=None, fprefix='streamer'):
        self.api = api or API()
        # set db connection
        # self.db = DB_Connection()

    # for each tweet streamed
    def on_status(self, status):
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
            link = 'https://www.twitter.com/' + \
                str(user_id) + '/status/' + str(tweet_id)

            # Connect to database
            db = DBConnect.DB_Connection()
            db.connect(password=keys.db_pass)

    # if theres an error

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False



# consumer key authentication
auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
# access key authentication
auth.set_access_token(keys.access_token, keys.access_token_secret)
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
