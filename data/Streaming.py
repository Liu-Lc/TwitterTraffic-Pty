from tweepy import API, OAuthHandler, Stream
from urllib3.exceptions import ProtocolError
# from DBConnect import DB_Connection  # class for connection the db
from Listener import SListener  # imports the Streaming Listener

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