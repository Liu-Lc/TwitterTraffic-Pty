#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Starts the streaming of tweets following the keywords:
@traficocpanama, traficocpanama, trafico panama.
See Listener on_status function to see processes done when 
a new tweet is streamed.

Created on Sun Apr 18 17:44 2021
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import time, sys
sys.path.append('./TweetData')
from datetime import timedelta

import pandas as pd
from multiprocessing import Process
from tweepy import API, OAuthHandler, Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError

from TweetData import DBConnect, keys, Tweet, \
    Preprocessing, Updater, Detection


class SListener(StreamListener):

    # initialize API
    def __init__(self, api=None, fprefix='streamer'):
        self.api = api or API()

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

            clas = Detection.get_classification(text)
            db.assign_classification(tweet.tweetid, True if clas['isIncident'] == 1 else False, 
                            True if clas['isAccident'] == 1 and clas['isIncident'] == 1 else False,
                            True if clas['isObstacle'] == 1 and clas['isIncident'] == 1 else False,
                            True if clas['isDanger'] == 1 and clas['isIncident'] == 1 else False)

            db.close_connection()
            print(text)

    # if theres an error
    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_data disconnects the stream
            return False


if __name__=='__main__':
    # Prepare STREAMING
    print('Starting.')

    # Update Tweets if the system fails
    # get last date and format it
    db = DBConnect.DB_Connection()
    db.connect(password=keys.db_pass)

    # gets last date
    last_date = db.query_date()
    last_date = (last_date - timedelta(days=1)).strftime('%Y-%m-%d')

    # get last week tweets
    print('Updating data.')
    start_time = time.time()

    past_tweets = Updater.get_tweets(from_date=last_date)

    # get tweets to dataframe
    # dict gets a dictionary of attributes and values
    data = pd.DataFrame([i.__dict__ for i in past_tweets])
    # get classification and category of each tweet
    data = Detection.get_classifications(data, 'text')

    # gets last id
    last_id = db.query('''
        SELECT MAX(TWEET_ID) 
        FROM TWEETS;''')[0][0]

    # iterates through updater tweets
    for index, row in data[data.tweetid > last_id].iterrows():
        # inserts tweet to db
        db.insert_tweet(row)
        # if the tweet is accident, inserts to database
        db.assign_classification(row.tweetid, True if row.isIncident == 1 else False, 
                        True if row.isAccident == 1 and row.isIncident == 1 else False,
                        True if row.isObstacle == 1 and row.isIncident == 1 else False,
                        True if row.isDanger == 1 and row.isIncident == 1 else False)

    # closes connection
    db.close_connection()

    end_time = time.time()
    print('Duration: %f\n' % (end_time-start_time))

    # Begin collecting data
    print('Starting stream.')
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

    try: 
        p = Process(target=stream.filter, 
            kwargs={'track':keywords, 'is_async':True})
        p.start()
        if input("Exit: ")=='q':
            print('Terminating.')
            p.terminate()
            print('Terminated.')
        
    # reconnect automantically if error rises
    # due to unstable network connection
    except (ProtocolError, AttributeError, KeyboardInterrupt) as e:
        print('CLOSING.')
