import psycopg2 as ps
from getpass import getpass

class DB_Connection():
    def __init__(self, database='traffictwt', user='admin', password=getpass()):
        connect(database, user, password)
    
    def connect(self, database='traffictwt', user='admin', password=getpass()):
        '''Connection to a database.'''
        try:
            self.conn = ps.connect(database=database, user=user, password=password)
            print('Connection succesful.')
        except: print('Error connecting to database.')

    def create_table(self):
        '''Creates table with tweet structure. '''
        commands = (# Table Tweet
                    '''CREATE TABLE IF NOT EXISTS Tweet(TWEET_ID BIGINT PRIMARY KEY,
                                                USER_ID BIGINT, USER_NAME TEXT,
                                                TWEET_TEXT TEXT,
                                                TWEET_CREATED TIMESTAMP WITH TIME ZONE,
                                                TWEET_LINK TEXT,
                                                TWEET_PLACE TEXT, TWEET_COORDINATES TEXT, 
                                                MEDIA1 TEXT, MEDIA2 TEXT, MEDIA3 TEXT, MEDIA4 TEXT;''')
        self.cursor = self.conn.cursor()
        try:
            for command in commands:
                # create tables
                self.cursor.execute(command)
            print('Tables recreated successfully.')
        except Exception as e: print(e)
        self.conn.commit()
        self.cursor.close()

    def insert_tweet(self, t):
        '''Inserts rows/data into Tweets table.'''
        self.cursor = self.conn.cursor()
        try:
            # insert tweet
            command = '''INSERT INTO TWITTERTWEET(TWEET_ID, TWEET_USER_ID, TWEET_TEXT,
                        TWEET_CREATED, TWEET_COORDINATES, TWEET_PLACE)
                        VALUES (%s, %s, %s, %s, %s, %s);'''
            self.cursor.execute(command, (t.tweetid, t.userid, t.username, \
                t.text, t.date, t.link, t.place, t.coords, \
                    t.media[0], t.media[1], t.media[2], t.media[3]))
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def close_connection(self):
        '''Closes connection. '''
        self.conn.close()
