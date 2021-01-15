import re, sys
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from getpass import getpass
from IPython.display import clear_output
from datetime import timedelta
from db_connection import DB_Connection

class Tweet(): pass

def get_tweet(card):
    '''Extract data from tweet card.'''
    t = Tweet()
    t.place = t.coords = ''
    t.userid = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    t.username = card.find_element_by_xpath('.//span').text
    t.text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text

    try:
        t.date = card.find_element_by_xpath('.//time').get_attribute('datetime')
        # date = datetime.strftime(date)
    except NoSuchElementException as e:
        return
    # link
    t.link = card.find_element_by_xpath('.//time/..').get_attribute('href')
    t.tweetid =  re.split('/', t.link)[5]

    t.media = []
    try:
        t.media.append(card.find_element_by_xpath('.//div[2]/div[2]/div[2]//video').get_attribute('poster'))
    except Exception: pass
    try:
        imgs = card.find_elements_by_xpath('.//div[2]/div[2]/div[2]//img')
        for img in imgs:
            t.media.append(img.get_attribute('src'))
    except Exception: pass
    for i in range(4-len(t.media)): t.media.append('')

    return t

# initializing db
db = DB_Connection()
# db.create_tables()

# start driver and go to twitter
driver = Chrome('C:\\Users\\lucia\\chromedriver.exe')
driver.get('https://www.twitter.com\login')
sleep(2)
# user and pass
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('Lc_L23')
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(getpass() + Keys.RETURN)
print('Logging in.')
sleep(2)

count = 0; starttime = time()
exit_var = False

# search the query
print('Searching.')
while True:
    res = db.query_date(False)
    res = (res + timedelta(days=1)).strftime('%Y-%m-%d')
    print('Restarting search: ' + res)
    search = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
    search.clear()
    search.send_keys('(from:traficocpanama) OR (@traficocpanama) until:'+ res + \
                ' -filter:replies -filter:retweets' + Keys.RETURN)
    sleep(2)
    driver.find_element_by_link_text('Latest').click()

    last_pos = driver.execute_script('return window.pageYOffset;')
    sleep(1)
    print('Starting scrape.')
    s1 = s0 = '0'

    while True:
        cards = driver.find_elements_by_xpath('//div[@aria-label="Timeline: Search timeline"]/div/div')
        for card in cards:
            try:
                tweet = get_tweet(card.find_element_by_xpath('.//div[@data-testid="tweet"]'))
                if len(db.query_id(tweet.tweetid))==0 or tweet==None:
                    db.insert_tweet(tweet)
                    count += 1
                    clear_output(wait=True)
                    nowtime = time()
                    sys.stdout.write('\r' + 'Tweets obtained: ' + str(count) + \
                        '\tETA:' + str(timedelta(seconds=nowtime-starttime)))
                    sys.stdout.flush()
            except Exception as e: print('\n', e)

        # get next scroll
        if len(s1)>6: break
        else:
            try:
                s1 = re.split(r'[\s()]', cards[-1].get_attribute('style'))[6]
                s1 = re.sub('[a-z]', '', s1)
                s1 = re.sub('\+', 'e', s1)
                s1 = str(int(float(s1) + 1000))
                driver.execute_script('window.scrollTo(0, ' + s1 +');')
            except:
                s0 = str(int(float(s0) + 2000))
                s0 = re.sub('\+', 'e', s0)
                driver.execute_script('window.scrollTo(0, ' + s0 +');')
            sleep(2)
            curr_pos = driver.execute_script('return window.pageYOffset;')
            if last_pos==curr_pos: exit_var = True; break
            else: last_pos = curr_pos
    if exit_var: break

print('\nEnd of search, closing.')
db.close_connection()