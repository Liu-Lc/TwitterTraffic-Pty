import psycopg2 as ps
from getpass import getpass
import time, datetime

class DB_Connection():
    def __init__(self, database='traffictwt', user='postgres'):
        self.connect(database, user)
    
    def connect(self, database='traffictwt', user='postgres', password=getpass()):
        '''Connection to a database.'''
        try:
            self.conn = ps.connect(database=database, user=user, password=password)
            print('Connection succesful.')
        except: print('Error connecting to database.')

    def create_tables(self):
        '''Creates table with tweet structure. '''
        commands = (# Table User
                    '''CREATE TABLE IF NOT EXISTS TwtUser(USER_ID TEXT PRIMARY KEY,
                                        USER_NAME TEXT);''',
                    # Table Tweet
                    '''CREATE TABLE IF NOT EXISTS TwtTweet(TWEET_ID BIGINT PRIMARY KEY,
                                                TWEET_USER_ID TEXT, TWEET_TEXT TEXT,
                                                TWEET_CREATED TIMESTAMP WITH TIME ZONE,
                                                TWEET_LINK TEXT,
                                                TWEET_PLACE TEXT, TWEET_COORDINATES TEXT, 
                                                MEDIA1 TEXT, MEDIA2 TEXT, MEDIA3 TEXT, MEDIA4 TEXT,
                                                CONSTRAINT FK_USER FOREIGN KEY(TWEET_USER_ID)
                                                 REFERENCES TwtUser(USER_ID));''')
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
            # insert user
            print(t.userid, t.username)
            command = '''INSERT INTO TWTUSER(USER_ID, USER_NAME)
                        VALUES ('%s', '%s') ON CONFLICT (USER_ID) 
                        DO NOTHING;''' % (t.userid, t.username)
            print(command)
            self.cursor.execute(command)
            # insert tweet
            command = '''INSERT INTO TWTTWEET(TWEET_ID, TWEET_USER_ID, TWEET_TEXT,
                        TWEET_CREATED, TWEET_LINK, TWEET_COORDINATES, TWEET_PLACE, 
                        MEDIA1, MEDIA2, MEDIA3, MEDIA4)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;'''
            self.cursor.execute(command, (t.tweetid, t.userid, \
                t.text, t.date, t.link, t.place, t.coords, \
                    t.media[0], t.media[1], t.media[2], t.media[3]))
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def close_connection(self):
        '''Closes connection. '''
        self.conn.close()