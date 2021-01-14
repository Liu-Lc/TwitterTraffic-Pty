import re
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from getpass import getpass
from IPython.display import clear_output
from datetime import timedelta

def get_tweet(card):
    '''Extract data from tweet card.'''
    userid = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    username = card.find_element_by_xpath('.//span').text
    text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text

    try:
        date = card.find_element_by_xpath('.//time').get_attribute('datetime')
        # date = datetime.strftime(date)
    except NoSuchElementException as e:
        return
    # link
    link = card.find_element_by_xpath('.//time/..').get_attribute('href')
    tweetid =  re.split('/', link)[5]

    media = []
    try:
        media.append(card.find_element_by_xpath('.//div[2]/div[2]/div[2]//video').get_attribute('poster'))
    except Exception: pass
    try:
        imgs = card.find_elements_by_xpath('.//div[2]/div[2]/div[2]//img')
        for img in imgs:
            media.append(img.get_attribute('src'))
    except Exception: pass

    tweet = (tweetid, userid, username, text, date, link, media)
    return tweet

# start driver and go to twitter
driver = Chrome('C:\\Users\\lucia\\chromedriver.exe')
driver.get('https://www.twitter.com\login')
# user and pass
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('Lc_L23')
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(getpass() + Keys.RETURN)
print('Logging in.')
sleep(2)

# search the query
print('Searching.')
search = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search.send_keys('(from:traficocpanama) OR (@traficocpanama) -filter:replies -filter:retweets' + Keys.RETURN)
driver.find_element_by_link_text('Latest').click()

last_pos = driver.execute_script('return window.pageYOffset;')
sleep(2)
print('Starting scrape.')
count = 0
starttime = time()

while True:
    cards = driver.find_elements_by_xpath('//div[@aria-label="Timeline: Search timeline"]/div/div')
    for card in cards:
        count += 1
        tweet = get_tweet(card.find_element_by_xpath('.//div[@data-testid="tweet"]'))
        clear_output(wait=True)
        nowtime = time()
        print('Tweets obtained:', str(count), \
            '\tETA:', str(timedelta(seconds=nowtime-starttime)))

    # get next scroll
    s = re.split(r'[\s()]', cards[-1].get_attribute('style'))[6]
    s = re.sub('[a-z]', '', s)
    driver.execute_script('window.scrollTo(0, ' + s +');')
    sleep(0.5)
    curr_pos = driver.execute_script('return window.pageYOffset;')
    if last_pos==curr_pos: break
    else: last_pos = curr_pos