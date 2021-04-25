#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...

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

# consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)
# access key authentication
auth.set_access_token(access_token, access_token_secret)
# set up API with authentication handler
api = API(auth, wait_on_rate_limit=True)

# Define the word to seach and date
search_word = "(from:traficocpanama) OR (@traficocpanama) -filter:replies -filter:retweets"

start_time = time.time()

# Collect tweets
tweets = Cursor(api.search,
                q=search_word,
                # since='2021-04-23',
                tweet_mode='extended').items()

all_info = [Tweet(t.id, t.user.screen_name, t.user.name, t.full_text, t.created_at,
                'https://www.twitter.com/' + str(t.user.screen_name) + '/status/' + str(t.id)) 
            for t in tweets]

end_time = time.time()

print(end_time-start_time)
print()
print(all_info[0])