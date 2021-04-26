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
from urllib3.exceptions import ProtocolError
from Listener import SListener  # imports the Streaming Listener
from keys import *

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