from tweepy import API 
from tweepy.streaming import StreamListener

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