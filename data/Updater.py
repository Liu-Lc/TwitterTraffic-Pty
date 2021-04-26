#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Updater file executes when the system hasn't been Streaming data
and the database needs to update the Tweets that didn't get during
certain period of time.

Created on Sat Apr 24 21:28 2021 21:28
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import json
import time
import pandas as pd
from tweepy import API, Cursor, OAuthHandler
from urllib3.exceptions import ProtocolError
import Tweet
from keys import *


def get_tweets():
   """Executes the function to get the last 7 days tweets.

   Args:
       None.

   Returns:
       Tweet array: Returns an array with all the Tweets found.
   """
   # consumer key authentication
   auth = OAuthHandler(consumer_key, consumer_secret)
   # access key authentication
   auth.set_access_token(access_token, access_token_secret)
   # set up API with authentication handler
   api = API(auth, wait_on_rate_limit=True)
   # Define the word to seach and date
   search_word = "(from:traficocpanama) OR (@traficocpanama) -filter:replies -filter:retweets"
   # Collect tweets
   tweets = Cursor(api.search,
                  q=search_word,
                  # since='2021-04-23',
                  tweet_mode='extended').items()
   all_tweets = [Tweet(t.id, t.user.screen_name, t.user.name, t.full_text, t.created_at,
                  'https://www.twitter.com/' + str(t.user.screen_name) + '/status/' + str(t.id)) 
               for t in tweets]
   return all_tweets
