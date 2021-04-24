from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy import Stream
from DBConnect import DB_Connection # class for connection the db
from urllib3.exceptions import ProtocolError

# keys for API
consumer_key = 'A5YS1UVZEbiIZdbiUKKageZKe'
consumer_secret = 'z13JcgAG0v8ratKmMVPrsLGNiDkM7XnyG2AWvTmf5agebGnodK'
access_token = '1344702616186589185-HG0juN3inE9vk3M4X52vFQ9ewWoNvj'
access_token_secret = 't9TOMRE3XzEdqj1hbmeqHlnMiddMVyuBO7dY5RvvKDmMZ'

# consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)
# access key authentication
auth.set_access_token(access_token, access_token_secret)
# set up API with authentication handler
api = API(auth, wait_on_rate_limit=True)

