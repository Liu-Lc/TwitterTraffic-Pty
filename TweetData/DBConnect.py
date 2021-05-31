import psycopg2 as ps
from getpass import getpass
import time, datetime

class DB_Connection():
    def __init__(self):
        pass
    
    def connect(self, database='traffictwt', user='postgres', password=None):
        '''Connection to a database.'''
        try:
            if password==None: password = getpass()
            self.conn = ps.connect(database=database, user=user, password=password)
            return True
        except: return False

    def create_tables(self):
        '''Creates table with tweet structure. '''
        commands = (# Table User
                    '''CREATE TABLE IF NOT EXISTS USERS(USER_ID TEXT PRIMARY KEY,
                                        USER_NAME TEXT);''',
                    # Table Tweet
                    '''CREATE TABLE IF NOT EXISTS TWEETS(TWEET_ID BIGINT PRIMARY KEY,
                                                TWEET_USER_ID TEXT, TWEET_TEXT TEXT,
                                                TWEET_CREATED TIMESTAMP WITH TIME ZONE,
                                                TWEET_LINK TEXT,
                                                TWEET_PLACE TEXT, TWEET_COORDINATES TEXT, 
                                                MEDIA1 TEXT, MEDIA2 TEXT, MEDIA3 TEXT, MEDIA4 TEXT,
                                                CONSTRAINT FK_USER FOREIGN KEY(TWEET_USER_ID)
                                                 REFERENCES TwtUser(USER_ID));''',
                    # Table Incident
                    '''CREATE TABLE IF NOT EXISTS INCIDENTS(INC_TWEET_ID BIGINT PRIMARY KEY,
                                                            INC_PLACE_ID BIGINT,
                                                            ISINCIDENT BOOLEAN,
                                                            ISACCIDENT BOOLEAN,
                                                            ISOBSTACLE BOOLEAN,
                                                            ISDANGER BOOLEAN,
                                                            CONSTRAINT FK_TWT_ID FOREIGN KEY(INC_TWEET_ID)
                                                                REFERENCES TwtTweet(TWEET_ID),
                                                            CONSTRAINT FK_PLACE_ID FOREIGN KEY(INC_PLACE_ID)
                                                                REFERENCES Place(PLACE_ID));''',
                    # Table Place
                    '''CREATE TABLE IF NOT EXISTS PLACE(PLACE_ID BIGINT PRIMARY KEY,
                                                        PLACE_NAME TEXT,
                                                        PLACE_LAT FLOAT,
                                                        PLACE_LONG FLOAT);''')
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
        '''Inserts rows/data into Tweets table. With attributes
            userid, username, tweetid, text, date, link'''
        self.cursor = self.conn.cursor()
        try:
            # insert tweet
            command = '''INSERT INTO TWEETS(TWEET_ID, USER_ID, USER_NAME,
                        TWEET_TEXT, TWEET_CREATED, TWEET_LINK)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;'''
            self.cursor.execute(command, (t.tweetid, t.userid, t.username,  \
                t.text, t.date, t.link))
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def insert_incident(self, t):
        '''Inserts incident data into the Incidents table.'''
        self.cursor = self.conn.cursor()
        try:
            # insert incident
            command = '''UPDATE TWEETS SET ISINCIDENT=TRUE, 
                        ISACCIDENT=%s, ISOBSTACLE=%s, ISDANGER=%s
                        WHERE TWEET_ID=%s;
                        '''
            self.cursor.execute(command, (t.isAccident, \
                                t.isObstacle, t.isDanger, t.tweetid))
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def insert_place(self, t):
        '''Inserts place data into Place table.'''
        self.cursor = self.conn.cursor()
        try:
            # insert incident
            command = '''INSERT INTO PLACE(place_name, street, town, district, lat, "long")
                        VALUES (%s, %s, %s, %s, %s, %s);'''
            self.cursor.execute(command, (t.name, t.street, \
                t.town, t.district, t.lat, t.long))
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def assign_place(self, id, place, street=None, no=None):
        '''Assigns place with regex strings.'''
        self.cursor = self.conn.cursor()
        command = '''UPDATE INCIDENTS SET PLACE=%d 
                         WHERE PLACE IS NULL AND text ~* '%s'
                         ''' % (id, place)
        if street!='': 
            # print('street: ' + street)
            command += " AND text ~* '" + street + "'"
        if no!='': 
            # print('street: ' + no)
            command += " AND text !~* '" + no + "'"
        command += ';'
        try:
            self.cursor.execute(command)
            print(command)
        except Exception as e: print(e)
        # commit changes and close cursor
        self.conn.commit()
        self.cursor.close()

    def query_id(self, tweetid):
        '''Returns id from query.'''
        results = ''
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('SELECT * FROM TWEETS WHERE TWEET_ID=' + 
                str(tweetid) + ';')
            results = self.cursor.fetchall()
            return results
        except Exception as e: print(e); return
        self.cursor.close()

    def query_date(self, last=True):
        '''Gets first or last date obtained.'''
        q = ''
        if last: q = '''SELECT TWEET_CREATED FROM TWEETS ORDER BY TWEET_CREATED
                    DESC LIMIT 1;'''
        else: q = '''SELECT TWEET_CREATED FROM TWEETS ORDER BY TWEET_CREATED
                    ASC LIMIT 1;'''
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(q)
            result = self.cursor.fetchone()[0]
            return result
        except Exception as e: print(e); return
        self.cursor.close()

    def query(self, q):
        '''Returns result from query.'''
        results = ''
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(q)
            results = self.cursor.fetchall()
            return results
        except Exception as e: print(e); return
        self.cursor.close()

    def query_all(self):
        '''Returns the whole dataset.'''
        command = '''SELECT * FROM TWEETS;'''
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(command)
            results = self.cursor.fetchall()
            return results
        except Exception as e: print(e); return
        self.cursor.close()

    def close_connection(self):
        '''Closes connection. '''
        self.conn.close()