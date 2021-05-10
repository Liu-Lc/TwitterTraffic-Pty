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

import pandas as pd
from tweepy import API, OAuthHandler, Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError

import DBConnect
import Detection
import keys
import Preprocessing
import Updater
import Tweet


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

            tweet = Tweet.Tweet(tweet_id, user_id, user_name, 
                text, tweet_created, link)

            # Connect to database
            db = DBConnect.DB_Connection()
            db.connect(password=keys.db_pass)
            db.insert_tweet(tweet)

            clas = Detection.get_classification()
            if row.isIncident==1:
                i = Tweet.Incident(row.tweetid, None, 
                    True if row.isAccident==1 else False, 
                    True if row.isObstacle==1 else False, 
                    True if row.isDanger==1 else False)
                db.insert_incident(i)

            db.close_connection()
            print(text)


    # if theres an error
    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False


##### Prepare STREAMING
print('Starting.')
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


##### Update Tweets if the system fails
# get last date and format it
db = DBConnect.DB_Connection()
db.connect(password=keys.db_pass)

# gets last date
last_date = db.query_date()
last_date = (last_date - timedelta(days=1)).strftime('%Y-%m-%d')

# get last week tweets
print('Updating data.')
past_tweets = Updater.get_tweets(from_date=last_date)

# get tweets to dataframe
# dict gets a dictionary of attributes and values
data = pd.DataFrame([i.__dict__ for i in past_tweets])
# get classification and category of each tweet
data = Detection.get_classifications(data, 'text')

# gets last id
last_id = db.query('''
    SELECT max(inc_tweet_id) 
    FROM public.twtincident;''')[0][0]

## iterates through updater tweets
for index, row in data[data.tweetid>last_id].iterrows():
    # inserts tweet to db
    db.insert_tweet(row)
    # if the tweet is accident, inserts to database
    if row.isIncident==1:
        i = Tweet.Incident(row.tweetid, None, 
            True if row.isAccident==1 else False, 
            True if row.isObstacle==1 else False, 
            True if row.isDanger==1 else False)
        db.insert_incident(i)

# closes connection
db.close_connection()


##### Begin collecting data
print('Starting stream.')
while True:
    # maintian connection unless interrupted
    try:
        stream.filter(track=keywords)
    # reconnect automantically if error arise
    # due to unstable network connection
    except (ProtocolError, AttributeError):
        continue
