#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Scraping file gets historical data from a certain seach of tweets
using Selenium Chrome WebDriver and stores it in a PostgreSQL database.

Created on Thy Jan 14 14:52 2021
@author: Lucia Liu (lucia.liu@utp.ac.pa)
"""

import re, sys
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from getpass import getpass
from IPython.display import clear_output
from datetime import timedelta
from DBConnect import DB_Connection
import Tweet
import Detection


class Scrape():
    def __init__(self):
        """Sets the database connection and initializes it.
        """
        # initializing db
        self.db = DB_Connection()
        self.db.connect()
        # db.create_tables()

    def get_tweet(self, card):
        """Extracts the data from the tweet card and sets the attributes.

        Args:
            card (Selenium WedElement): Group element obtained from Selenium Webdriver
            (find_element functions).

        Returns:
            Tweet: Tweet object (see Tweet.py) with assigned attributes.
        """
        
        ## GET USER INFO AND TWEET TEXT
        userid = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        username = card.find_element_by_xpath('.//span').text
        text = card.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]').text
        ## GET TIME DATA
        try:
            date = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            # if it doesn't have date, means
            # it's an ad or something else
            return
        ## GET LINK
        link = card.find_element_by_xpath('.//time/..').get_attribute('href')
        # tweet id is in the tweet link
        tweetid =  re.split('/', link)[5]
        ## CREATE EMPTY OBJECT
        t = Tweet.Tweet(tweetid, userid, username, text, date, link) # empty object
        ## RETURN TWEET INFO
        return t

    def start_scrape(self, date_from=None, date_until=''):
        """Method that starts the scraping process and inserts the data
        into the database.

        Args:
            date_from (DateTime Date, optional): Sets the date the search starts from. Defaults to None.
            date_until (String, optional): Sets the date the search ends until. Defaults to None.

        Returns:
            None.
        """
        ## start driver and go to twitter
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        driver = Chrome('C:\\Users\\lucia\\chromedriver.exe')
        driver.get('https://www.twitter.com\login')
        sleep(5) # time to load
        ## user and pass
        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys('Lc_L23' + Keys.RETURN)
        sleep(2)
        password = driver.find_element_by_xpath('//input[@name="password"]')
        password.send_keys(getpass('Twt pass: ') + Keys.RETURN)
        print('Logging in.')
        sleep(5)
        # temp variables
        count = 0; count_i = 0; starttime = time()
        exit_var = False
        ## SEARCH QUERY
        print('Searching.')
        while True: # loop results
            ## query text
            query_text = '(from:traficocpanama) OR (@traficocpanama) '
            ## get last date in database
            if date_from==None:
                date_from = self.db.query_date(last=True)
            # formats date for search and minus a day
            date_from = (date_from - timedelta(days=1)).strftime('%Y-%m-%d')
            print('From date: ' + date_from)
            query_text += 'since:' + date_from
            # checks if a limit date was given
            if date_until!='':
                query_text += ' until:' + date_until
            query_text += ' -filter:replies -filter:retweets'
            print(query_text)
            # gets search box element
            driver.find_element_by_xpath('//label[@data-testid="SearchBox_Search_Input_label"]').click()
            try:
                driver.find_element_by_xpath('//label[@data-testid="SearchBox_Search_Input_label"]//div[@role="button"]').click()
            except: pass
            driver.find_element_by_xpath('//label[@data-testid="SearchBox_Search_Input_label"]').click()
            search = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
            ## sends query text
            search.send_keys(query_text + Keys.RETURN)
            driver.refresh()
            sleep(2)
            # order by latest dates
            driver.find_element_by_link_text('Latest').click()
            # sets position variable
            last_pos = driver.execute_script('return window.pageYOffset;')
            sleep(2)
            # order by latest dates
            try:
                driver.find_element_by_link_text('Latest').click()
                driver.execute_script('window.scrollTo(0, 3000);')
                sleep(1)
                driver.execute_script('window.scrollTo(0, 6000);')
                sleep(1)
                driver.execute_script('window.scrollTo(0, 9000);')
                sleep(1)
                driver.find_element_by_link_text('Latest').click()
            except: pass
            driver.refresh()
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
                        tweet = self.get_tweet(card.find_element_by_xpath('.//article[@data-testid="tweet"]'))
                        # checks if the tweet is valid
                        if tweet!=None: # len(self.db.query_id(tweet.tweetid))!=0 or 
                            # inserts tweet in database
                            self.db.insert_tweet(tweet)
                            count += 1 # counter for tweets obtained
                            clas = Detection.get_classification(tweet.text)
                            self.db.assign_classification(tweet.tweetid, True if clas['isIncident'] == 1 else False, 
                                            True if clas['isAccident'] == 1 and clas['isIncident'] == 1 else False,
                                            True if clas['isObstacle'] == 1 and clas['isIncident'] == 1 else False,
                                            True if clas['isDanger'] == 1 and clas['isIncident'] == 1 else False)
                            count_i += 1 if clas['isIncident'] else 0
                            clear_output(wait=True)
                            nowtime = time()
                            # resume
                            sys.stdout.write('\r' + 'Tweets obtained: ' + str(count) + \
                                # '\tIncidents: ' + str(count_i) + \
                                '\tETA:' + str(timedelta(seconds=nowtime-starttime)))
                            sys.stdout.flush()
                    # if the card is unavailable or something, skips
                    except Exception as e: print('\nScraping.start_scrape module line 173:', e)
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

if __name__=='__main__':
    print('Scraping.')
    scrape = Scrape()
    scrape.start_scrape()
    print('Finished.')