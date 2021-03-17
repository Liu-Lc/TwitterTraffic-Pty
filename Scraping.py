import re, sys
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from getpass import getpass
from IPython.display import clear_output
from datetime import timedelta
from DBConnect import DB_Connection

class Tweet(): pass

class Scrape():
    def __init__(self):
        # initializing db
        self.db = DB_Connection()
        # db.create_tables()

    def get_tweet(self, card):
        '''Extract data from tweet card.'''
        ## CREATE EMPTY OBJECT
        t = Tweet() # empty object
        ## GET USER INFO AND TWEET TEXT
        t.place = t.coords = '' # empty place and coords
        t.userid = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        t.username = card.find_element_by_xpath('.//span').text
        t.text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        ## GET TIME DATA
        try:
            t.date = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException as e:
            # if it doesn't have date, means
            # it's an ad or something else
            return
        ## GET LINK
        t.link = card.find_element_by_xpath('.//time/..').get_attribute('href')
        # tweet id is in the tweet link
        t.tweetid =  re.split('/', t.link)[5]
        ## GET MEDIA FILES
        t.media = []
        try: # gets video files if exists
            t.media.append(card.find_element_by_xpath('.//div[2]/div[2]/div[2]//video').get_attribute('poster'))
        except Exception: pass
        try: # gets image files if exist
            imgs = card.find_elements_by_xpath('.//div[2]/div[2]/div[2]//img')
            for img in imgs:
                t.media.append(img.get_attribute('src'))
        except Exception: pass
        # check if there are links, if not then assign empty
        for i in range(4-len(t.media)): t.media.append('')
        ## RETURN TWEET INFO
        return t

    def start_scrape(self, date_from=None, date_until=None):
        '''Method to start the scraping process'''
        ## start driver and go to twitter
        driver = Chrome('C:\\Users\\lucia\\chromedriver.exe')
        driver.get('https://www.twitter.com\login')
        sleep(2) # time to load
        ## user and pass
        username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username.send_keys('Lc_L23')
        password = driver.find_element_by_xpath('//input[@name="session[password]"]')
        password.send_keys(getpass() + Keys.RETURN)
        print('Logging in.')
        sleep(2)
        # temp variables
        count = 0; starttime = time()
        exit_var = False
        ## SEARCH QUERY
        print('Searching.')
        while True: # loop results
            ## query text
            query_text = '(from:traficocpanama) OR (@traficocpanama) '
            ## get last date in database
            if date_from=='':
                date_from = self.db.query_date(last=True)
            # formats date for search and minus a day
            date_from = (date_from - timedelta(days=1)).strftime('%Y-%m-%d')
            print('From date: ' + date_from)
            query_text += 'since:' + date_from
            # checks if a limit date was given
            if date_until!='':
                query_text += 'until:' + date_until
            query_text += ' -filter:replies -filter:retweets'
            # gets search box element
            search = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
            search.clear()
            ## sends query text
            search.send_keys(query_text + Keys.RETURN)
            sleep(2)
            # order by latest dates
            driver.find_element_by_link_text('Latest').click()
            # sets position variable
            last_pos = driver.execute_script('return window.pageYOffset;')
            sleep(1)
            print('Starting scrape.')
            s1 = s0 = '0' # scroll level
            ## starts loop
            while True:
                # gets the cards (available tweets)
                cards = driver.find_elements_by_xpath('//div[@aria-label="Timeline: Search timeline"]/div/div')
                for card in cards: # loops in each card
                    try:
                        # gets the tweet info from a card
                        tweet = get_tweet(card.find_element_by_xpath('.//div[@data-testid="tweet"]'))
                        # checks if the tweet is valid
                        if len(self.db.query_id(tweet.tweetid))==0 or tweet==None:
                            # inserts tweet in database
                            self.db.insert_tweet(tweet)
                            count += 1 # counter for tweets obtained
                            clear_output(wait=True)
                            nowtime = time()
                            # resume
                            sys.stdout.write('\r' + 'Tweets obtained: ' + str(count) + \
                                '\tETA:' + str(timedelta(seconds=nowtime-starttime)))
                            sys.stdout.flush()
                    # if the card is unavailable or something, skips
                    except Exception as e: print('\n', e)
                # get next scroll
                if len(s1)>6: break
                else:
                    try: # checks scroll level
                        s1 = re.split(r'[\s()]', cards[-1].get_attribute('style'))[6]
                        s1 = re.sub('[a-z]', '', s1)
                        s1 = re.sub('\+', 'e', s1)
                        s1 = str(int(float(s1) + 1000))
                        # scrolls window
                        driver.execute_script('window.scrollTo(0, ' + s1 +');')
                    except: # if scroll level info not available
                        s0 = str(int(float(s0) + 2000)) # scrolls 2000 points
                        s0 = re.sub('\+', 'e', s0)
                        driver.execute_script('window.scrollTo(0, ' + s0 +');')
                    sleep(2)
                    # sets current position
                    curr_pos = driver.execute_script('return window.pageYOffset;')
                    # if reached end of page = break loop
                    if last_pos==curr_pos:
                        # set variable to break next loop
                        exit_var = True; break
                    else: last_pos = curr_pos
            # break loop if reached end
            if exit_var: break
        # if loop broken, end search
        print('\nEnd of search, closing.')
        # close connection
        self.db.close_connection()