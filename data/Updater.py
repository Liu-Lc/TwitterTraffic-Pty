#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Updater file executes when the system hasn't been Streaming data
and the database needs to update the Tweets that didn't get during
certain period of time.

Created on Sat Apr 24 21:28 2021 21:28
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

from tweepy import OAuthHandler, API, Cursor
import json
from urllib3.exceptions import ProtocolError
import pandas as pd
import time
from keys import *
import Tweet

def get_tweets(api):
   """Executes the function to get the last 7 days tweets.

   Args:
       api (tweepy.API): Gets the api with the authentication.

   Returns:
       Tweet array: Returns an array with all the Tweets found.
   """
   # set up API with authentication handler
   api = api
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