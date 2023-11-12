from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path

import pickle
from selenium.webdriver.common.action_chains import ActionChains

from search import search_tweet_for_better_rt ,  get_giveaway_url
from selenium.webdriver.common.by import By
from get_tweet import *
import traceback

import feedparser
from random import randint

with open("configuration.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    
MINTIME = data["min_time"]
MAXTIME = data["max_time"]

class Scraper:
    
    wait_time = 5
    headless = data["headless"]
    options = webdriver.ChromeOptions()
    if headless == True:
        options.add_argument('headless')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    
    driver = webdriver.Chrome(options=options)  # to open the chromedriver    
    #options = webdriver.FirefoxOptions()
    #options.headless = False

    #driver = webdriver.Firefox(options=options)

    username_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
    
    button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
    password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div'
    test_tweet = 'https://twitter.com/Twitter/status/1580661436132757506'
    like_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[3]/div'
    cookie_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div/span/span'
    notification_button_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span/span'
    reetweet_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[2]/div'
    reetweet_confirm_button_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/span'
    comment_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[1]/div'
    textbox_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
    follow_button_xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div"
    unfollow_nbr = 0

def get_news():
    try:
        with open("configuration.yml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        url_list = data["flux_rss"]
        sentence_to_tweet = data["setence_to_tweet"]
        
        l = url_list[randint(0,len(url_list) - 1)]
        news_feed = feedparser.parse(l)

        news_title = []
        news_link = []
        idx = 0
        for entry in news_feed.entries:
            if idx != 0:
                break
            news_title.append(entry.title)
            news_link.append(entry.link)
            idx = idx + 1

        try:
            rdm_news = randint(0,len(news_title)) - 1
            return(news_title[rdm_news],news_link[rdm_news])
        except:
            try:
                return(news_title[0],news_link[0])
            except:
                return (sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)], "")
    except:
        return(sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)] , "")

def login(S,_username,_password):

    try:
        S.driver.get("https://twitter.com/i/flow/login")
        print("Starting Twitter")
        #USERNAME
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.username_xpath)))

        username = S.driver.find_element(By.XPATH,S.username_xpath)
        username.send_keys(_username)    
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.button_xpath)))


        #FIRST BUTTON

        button = S.driver.find_element(By.XPATH,S.button_xpath)
        button.click()
        print("button click")


        #PASSWORD

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.password_xpath)))
        
        password = S.driver.find_element(By.XPATH,S.password_xpath)
        password.send_keys(_password)
        print("password done")


        #LOGIN BUTTON

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.login_button_xpath)))
        
        login_button = S.driver.find_element(By.XPATH,S.login_button_xpath)
        login_button.click()
        print("login done")
        return True
        #print("Closing Twitter")
    except:
        time.sleep(5)
        for i in range(3):
            time.sleep(5)
            if check_login_good(S) == True:
                return True
        
        if retry_login(S,_username,_password) == True:
            return True
        
        print("wrong username of password")
        print("skipping the account")
        return False

def retry_login(S,_username,_password):

    try:
        S.driver.get("https://twitter.com/i/flow/login")
        #USERNAME
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.username_xpath)))

        username = S.driver.find_element(By.XPATH,S.username_xpath)
        username.send_keys(_username)    
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.button_xpath)))


        #FIRST BUTTON

        button = S.driver.find_element(By.XPATH,S.button_xpath)
        button.click()


        #PASSWORD

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.password_xpath)))
        
        password = S.driver.find_element(By.XPATH,S.password_xpath)
        password.send_keys(_password)


        #LOGIN BUTTON

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.login_button_xpath)))
        
        login_button = S.driver.find_element(By.XPATH,S.login_button_xpath)
        login_button.click()
        return True
        #print("Closing Twitter")
    except:
        time.sleep(5)        
        print("reloging failed")
        return False

def check_login_good(selenium_session):
    try:
        selenium_session.driver.get("https://twitter.com/home")
        element = WebDriverWait(selenium_session.driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Notifications_Link"]')))
        return True
    except Exception as e:
        
        return False
 
def accept_coockie(S):
    try:
        S.driver.get(S.test_tweet)

        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.cookie_button_xpath)))
        
        cookie_button = S.driver.find_element(By.XPATH,S.cookie_button_xpath)
        cookie_button.click()

    except:
        pass    
    
    
    print("coockie done")


def accept_notification(S):
    try:
        S.driver.get(S.test_tweet)

        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.notification_button_xpath)))
        
        cookie_button = S.driver.find_element(By.XPATH,S.notification_button_xpath)
        cookie_button.click()
    except:
        pass    
    try:
        S.driver.get(S.test_tweet)

        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.cookie_button_xpath)))
        
        cookie_button = S.driver.find_element(By.XPATH,S.cookie_button_xpath)
        cookie_button.click()

    except:
        pass    
    
    print("notification done")
    
 
def like_a_tweet(S,url):

    try:
        S.driver.get(url)
        try:
            element = WebDriverWait(S.driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="unlike"]')))
            like_button = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="unlike"]')
            return False
        except:
            element = WebDriverWait(S.driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="like"]')))
        
            like_button = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="like"]')
            like_button.click()
            return True 
        
    except:
        print("Bref like" * 10)
        return None



def reetweet_a_tweet(S,url):

    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="retweet"]')))
        
        reetweet_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
        reetweet_button.click()

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="retweetConfirm"]')))
        
        reetweet_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="retweetConfirm"]')
        reetweet_button.click()
        
        print("reetweet done")
    except:
        print("Bref rt")

def comment_a_tweet(S,url,text):

    try:

        S.driver.get(url)
        pos = 0
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
        
        tweet_info = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
        for i in range(len(tweet_info)):
            r = tweet_info[i]
            if url.split("twitter.com")[1] in str(r.get_attribute("outerHTML")):
                pos = i
                break
        
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="reply"]')))
        comment_button = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')
        comment_button[pos].click()
        time.sleep(5)
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
        textbox = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        S.driver.execute_script("arguments[0].scrollIntoView();", textbox)
        time.sleep(S.wait_time)
        for t in text:
            textbox.send_keys(t)
            #time.sleep(0.02)
        textbox.send_keys(" ")
        textbox.send_keys(Keys.RETURN)
        time.sleep(1)
        #textbox.click()
        #print("ok 2")
        time.sleep(2)
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
        wait = WebDriverWait(S.driver, 10)
        target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
        S.driver.execute_script("arguments[0].scrollIntoView();", target_element)
        target_element.click()
        time.sleep(5)
        print("comment done")
    except:
        print("Bref comment")

def make_a_tweet(S,text):
    try:
        S.driver.get("https://twitter.com/compose/tweet")
        time.sleep(10)
        #print("coment part one")
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
        
        textbox = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        textbox.click()
        time.sleep(S.wait_time)
        textbox.send_keys(text)
        
        #print("coment part two")
        time.sleep(5)
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))

        wait = WebDriverWait(S.driver, 10)
        target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))

        S.driver.execute_script("arguments[0].scrollIntoView();", target_element)

        target_element.click()

        #print("comment part three")
        print("Tweet done")
    except:
        print("Bref tweet")    

def unfollow_an_account(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'[data-testid="placementTracking"]')))
        unfollow_button = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="placementTracking"]')
        if unfollow_button.text != "Abonné" and unfollow_button.text != "Following":
            return (True)
        unfollow_button.click()
        click_confirm = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="confirmationSheetConfirm"]')
        click_confirm.click()
    except Exception as e:
        #print("Unfollow account error")
        return (False)


def follow_an_account(S,account,t):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, t).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'[data-testid="placementTracking"]')))
        follow_button = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="placementTracking"]')
        if follow_button.text != "Follow" and follow_button.text != "Suivre":
            print("You already follow the account")
            return (True)
        follow_button.click()
        time.sleep(randint(MINTIME,MAXTIME))
        if MAXTIME < 4:
            time.sleep(3)
        
        print("You've followed another account " + account)
        return True
    except Exception as e:
        print("Bref follow")
        return (False)

def get_only_account(s):
    l = []
    for i in range(len(s)):
        if s[i][0] == "@":
            l.append(s[i])
    return (l)

def get_tweet_text(S,url):
    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]')))
        return (str(element.text))
    except Exception as e:
        print("Bref text")
        return ("je")

def get_tweet_username(S,url):
    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="User-Name"]')))
        account = str(element.text).split("@")
        return (account[1])
    except:
        print("Bref username")
        return ("")


def get_tweet_info(selenium_session,url):
    tweet_info_dict = {"username":"",
    "text":"",}

    try:
        selenium_session.driver.get(url)
        user_tweet = url.split("/")[3]
        
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
        tweet_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
        pos = 0
        for i in range(len(tweet_info)):
            r = tweet_info[i]
            if url.split("twitter.com")[1] in str(r.get_attribute("outerHTML")):
                pos = i
                break
        
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))        
        
        
        _tweet_data = selenium_session.driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
        _tweet_text = selenium_session.driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweetText"]')
        
        tweet_data = str(_tweet_data[pos].text).split("\n")
        tweet_text = str(_tweet_text[pos].text)
        
        usr = tweet_data[1]
        if "@" not in usr:
            usr = tweet_data[0]
        tweet_info_dict = {"username":usr,
        "text":tweet_text,}
        return (tweet_info_dict)
    except Exception as e:
        print("Bref tweet info")
        return({"username":"x",
    "text":"x",})

def get_who_to_follow(S,url,text,username):

    try:
        a = username
        b = text
        c = list_of_account_to_follow(a ,b.strip().replace("\n",""))
        c = c.replace(",","").strip()
        c = c.split(" ")
        d = []
        for elem in c:
            if elem.lower() not in d:
                d.append(elem.lower())
        return(d)
    except:
        print("Bref userrrr")
        return("")

def get_elem_from_list(list_,elem_):
    for l in list_:
        if elem_ in l:
            return (l)
    return ("")

def parse_number(num):
    num = str(num)
    num = num.lower()
    if "b" in num:
        if "." in num:
            num  = num.replace(".","").replace("b","")
            num  = num + "00000000"
            
        else:
            num = num.replace("b","")
            num  = num + "000000000"
            
    elif "m" in num:
        if "." in num:
            num  = num.replace(".","").replace("m","")
            num  = num + "00000"

        else:
            num = num.replace("m","")
            num  = num + "000000"
    
    elif "k" in num:
        if "." in num:
            num  = num.replace(".","").replace("k","")
            num = num + "00"
        else:
            num = num.replace("k","")
            num = num + "000"
    else:
        if "." in num:
            num  = num.replace(".","")
    if "," in num:
        num = num.replace(",","")
    return num


def get_list_of_my_followings(S,user):
    try:
        nb_of_followings = get_user_following_count(S,user)
        S.driver.get("https://twitter.com/"+user+"/following")
        run  = True
        list_of_user = []
        selenium_data = []
        account = ""
        nb = 0
        while run:
            try:
                element = WebDriverWait(S.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="UserCell"]')))
                tweets_username = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="UserCell"]')
                last_user = tweets_username[len(tweets_username) - 1]
                for tweet_username in tweets_username:
                
                    if tweet_username not in selenium_data:
                        try:
                            parsing_user =str(tweet_username.text).split("\n")
                            account = parsing_user[1]
                            list_of_user.append(account.replace("@",""))
                            selenium_data.append(tweet_username)
                            S.driver.execute_script("arguments[0].scrollIntoView();", tweet_username)
                            nb+=1
                            time.sleep(0.025)
                        except:
                            time.sleep(0.025)
                            pass
                        if nb >= nb_of_followings:
                            print("Your following listing done")
                            return(list_of_user)
            except Exception as e:
                print("Your following listing failed")
                return (list_of_user)
        return(list_of_user)
    except Exception as e:
        print("Your following listing failed")
        return(False)

def get_user_following_count(S,user):
    try:
        num = "0123456789"
        S.driver.get("https://twitter.com/"+user)
        element = WebDriverWait(S.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="UserName"]')))
        following_count = ""

        following_count = S.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span")
        following_count = following_count.text
        following_count=following_count.replace(" ","")
        following_count = parse_number(following_count)
        return int(following_count)
    except Exception as e:
        try:
            num = "0123456789"
            S.driver.get("https://twitter.com/"+user)
            element = WebDriverWait(S.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="UserName"]')))
            following_count = ""
            try:
                f = parse_number(get_elem_from_list(S.driver.find_element(By.CSS_SELECTOR, '[data-testid="primaryColumn"]').text.split("\n"),"abonnements").split(" "))
                for n in f:
                    if n in num:
                        following_count = following_count + n
                return (int(following_count))
            except:
                following_count = parse_number(get_elem_from_list(S.driver.find_element(By.CSS_SELECTOR, '[data-testid="primaryColumn"]').text.split("\n"),"Following").split(" ")[0])
                return int(following_count)            
        except:
            print("Following count error")
            #traceback.print_exc()
            return(0)


def check_if_good_account_login(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'[data-testid="userActions"]')))
        u = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="userActions"]')
        print("Bot didn't log in to the right account let's retry login")
        return False
    except Exception as e:
        return True

def forever_loop():
    while True:
        try:
            main_one()
        except Exception as e:
            print("Flop " + str(e))
            time.sleep(600)
        time.sleep(randint(86400,172800))

def main_one():
    print("Inside main one")
    giveaway_done = 0
    with open("configuration.yml", "r",encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    print("Starting the program")
    print("Searching for Giveaway")
    username_info = data["account_username"]
    password_info = data["account_password"]
    sentence_to_tweet = data["setence_to_tweet"]
    random_rt_and_tweet = data["random_retweet_and_tweet"]
    random_tweet_nb = data["random_tweet_nb"]
    random_retweet_nb = data["random_retweet_nb"]
    crash_or_no = data["crash_or_no"]
    random_action = data["random_action"]
    human = data["human"]
    idxx = 0
    account_num = 0
    tweet_txt = []
    tweet_username = []
    crash_follow = []
    t_follow = []
    tt_follow = []
    ttt_follow = []
    tttt_follow = []
    tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not = [] , [] , [] , [] , []
    t_comment_or_not , t_full_comment, t_follows = [] , [] , []
    alph_follow = []
    for i in range(len(username_info)):
        account_num+=1
        print("Connecting to " + str(username_info[i]))
        time.sleep(1)
        S = Scraper()
        
        if login(S,username_info[i],password_info[i]) == False:
            account_num = 0
            continue
        time.sleep(3)
        if check_login_good(S) == False:
            print(f"The account is locked or password of {username_info[i]} is wrong change it on the configuration.yml file")
            print("Skipping the account")
            account_num = 0
            continue
        accept_coockie(S)
        time.sleep(S.wait_time)    
        accept_notification(S)
        time.sleep(S.wait_time)
        accept_coockie(S)
        time.sleep(S.wait_time)
        
        for w in range(10):
            if check_if_good_account_login(S,username_info[i]) == False:
                time.sleep(2)
                S = Scraper()
                if login(S,username_info[i],password_info[i]) == False:
                    account_num = 0
                    continue
                time.sleep(3)
                if check_login_good(S) == False:
                    print(f"The account is locked or password of {username_info[i]} is wrong change it on the configuration.yml file")
                    print("Skipping the account")
                    account_num = 0
                    continue
                accept_coockie(S)
                time.sleep(S.wait_time)    
                accept_notification(S)
                time.sleep(S.wait_time)
                accept_coockie(S)
                time.sleep(S.wait_time)
            else:
                break
                    
        giveaway_g = 0
        follow_nbr = 0

        nb_of_following_t1 = 0
        less_than_4500 = 0
        big_follow = 0
        for j in range(5):
            x = get_user_following_count(S,username_info[i])
            if x < 4500 or x > 9999:
                less_than_4500+=1
            else:
                big_follow = x

        
        if less_than_4500 >= 3:
            nb_of_following_t1 = 1
        
        else:
            nb_of_following_t1 = big_follow + 1

        account_to_unfollow = ""
        if nb_of_following_t1 > 4500:
            all_my_following = get_list_of_my_followings(S,username_info[i])
            if all_my_following != False:    
                print("You got to much following bot going to unfollow some people")
                for j in range(1000):
                    account_to_unfollow = all_my_following[len(all_my_following) - 1 - j]
                    #print("unfollowing: " , account_to_unfollow , " nb: " , j+1)
                    unfollow_an_account(S,account_to_unfollow)
                    time.sleep(3)
                nb_of_following_t2 = get_user_following_count(S,username_info[i])    
                print("Unfollow done bot unfollowed " , str(nb_of_following_t1-nb_of_following_t2) , " accounts you now have " , nb_of_following_t2 , " followings")              
                print("Bot sleeping 20 minutes to avoid twitter rate limit")
                time.sleep(60*20)
        if crash_or_no == True:
#            print("hellloooooooo ")
            if account_num == 1:
                tweet_from_url = print_file_info("recent_url.txt").split("\n")
                for t in tweet_from_url:
                    info = get_tweet_info(S,t)
                    tweet_txt.append(info["text"])
                    time.sleep(1)
                    crash_follow.append(info["username"])
                    for g in get_who_to_follow(S,t,info["text"],info["username"]):
                        tt_follow.append(g)
                
                for tt in tt_follow:
                    t_follow.append(tt)
            t_comment_or_not , t_full_comment, t_follows = giweaway_from_url_file(tweet_txt,crash_follow,S)
            
            if len(t_follow) == 0:
                print("No giveaway found...")
                if random_rt_and_tweet == True:
                    if random_action == True and random_tweet_nb > 0:
                        random_tweet_nb = randint(1,random_tweet_nb)
                    for i in range(random_tweet_nb):
                        info , info_link = get_news()
                        make_a_tweet(S,info+" "+info_link)
                        time.sleep(randint(MINTIME,MAXTIME))
                    make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                    try:
                        rt_url = search_tweet_for_better_rt(S)
                    
                        for i in range(len(rt_url)):
                            like = like_a_tweet(S,rt_url[i])
                            if like == True:            
                                reetweet_a_tweet(S,rt_url[i])
                            time.sleep(randint(MINTIME,MAXTIME))
                    except:
                        print("ok")
                continue
            try:
                t_follows.remove("")
            except:
                print("Something bad happend the program need to stop")
            for t in t_follows:
                if t != "":
                    t_follow.append(t.replace(" ",""))
            
            t_follow = list(dict.fromkeys(t_follow))
            for c in t_follow:
                if c.lower() not in ttt_follow:
                    ttt_follow.append(c.lower())
            ttt_follow = list(dict.fromkeys(ttt_follow))
            
            try:
                ttt_follow = get_a_better_list(t_follow)
            except:
                pass
            
            
            for i in range(len(ttt_follow)):
                if ttt_follow[i] != "" and ttt_follow[i].lower() not in tttt_follow:
                    if ttt_follow[i].lower().replace("@","") not in tttt_follow:
                        tttt_follow.append(ttt_follow[i])

            alph_list = int(len(tttt_follow)/2)

            for i in range(alph_list):
                follow_nbr +=1
                print("Account n " + str(follow_nbr) + " / " + str(len(tttt_follow)) + " account name: " + tttt_follow[i])
                follow_an_account(S,tttt_follow[i],2)
                alph_follow.append(tttt_follow[i].lower())

            if len(tttt_follow) > 80:
                time.sleep(120)

            for t in tweet_from_url:
                print("Giveaway number " + str(giveaway_g) + " / " + str(len(tweet_from_url)) + " all giveaway (even the one already done) " + str(giveaway_done))
                like = like_a_tweet(S,t)
                time.sleep(S.wait_time)    
                if like == True:
                    giveaway_done  += 1
                    giveaway_g += 1
                    reetweet_a_tweet(S,t)
                    #time.sleep(S.wait_time)        
                    try:       
                        if t_comment_or_not[idxx] == True:
                            comment_a_tweet(S,t,t_full_comment[idxx])
                        time.sleep(randint(MINTIME,MAXTIME))
                    except:
                        print("An error happend skiping this comment")
                else:
                    giveaway_done  += 1
                    print("You have already like the tweet")
                    time.sleep(2)
                if giveaway_g % 10 == 0 and giveaway_g > 1 and human == True:
                    time.sleep(5400)
                print(idxx)
                idxx = idxx + 1
            
            for account_to_follow in tttt_follow:
                print("Account n " + str(follow_nbr) + " / " + str(len(tttt_follow)) + " account name: " + account_to_follow)
                if account_to_follow.lower() not in alph_follow:
                    follow_an_account(S,account_to_follow,2)
                    follow_nbr +=1            
            
            if random_rt_and_tweet == True:
                if random_action == True and random_tweet_nb > 0:
                    random_tweet_nb = randint(1,random_tweet_nb)
                for i in range(random_tweet_nb):
                    info , info_link = get_news()
                    make_a_tweet(S,info+" "+info_link)
                    time.sleep(randint(MINTIME,MAXTIME))
                make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                try:
                    rt_url = search_tweet_for_better_rt(S)
                
                    for i in range(len(rt_url)):
                        like = like_a_tweet(S,rt_url[i])
                        if like == True:            
                            reetweet_a_tweet(S,rt_url[i])
                        time.sleep(randint(MINTIME,MAXTIME))
                except:
                    print("ok")
        
        if crash_or_no == False:
            if account_num == 1:
                tweet_from_url = get_giveaway_url(S)
                for t in tweet_from_url:
                    info = get_tweet_info(S,t)
                    tweet_txt.append(info["text"])
                    time.sleep(1)
                    crash_follow.append(info["username"])
                    for g in get_who_to_follow(S,t,info["text"],info["username"]):
                        tt_follow.append(g)
                for tt in tt_follow:
                    t_follow.append(tt)

            else:
                tweet_from_url = print_file_info("recent_url.txt").split("\n")
            
            t_comment_or_not , t_full_comment, t_follows = giweaway_from_url_file(tweet_txt,crash_follow,S)
            if len(t_follow) == 0:
                print("No giveaway found...")
                if random_rt_and_tweet == True:
                    if random_action == True and random_tweet_nb > 0:
                        random_tweet_nb = randint(1,random_tweet_nb)
                    for i in range(random_tweet_nb):
                        info , info_link = get_news()
                        make_a_tweet(S,info+" "+info_link)
                        time.sleep(randint(MINTIME,MAXTIME))
                    make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                    try:
                        rt_url = search_tweet_for_better_rt(S)

                        for i in range(len(rt_url)):
                            like = like_a_tweet(S,rt_url[i])
                            if like == True:            
                                reetweet_a_tweet(S,rt_url[i])
                            time.sleep(randint(MINTIME,MAXTIME))
                    except:
                        print("ok")
                continue
            try:
                t_follows.remove("")
            except:
                print("Something bad happend the program need to stop")
            for t in t_follows:
                if t != "":
                    t_follow.append(t.replace(" ",""))
            
            t_follow = list(dict.fromkeys(t_follow))
            for c in t_follow:
                if c.lower() not in ttt_follow:
                    ttt_follow.append(c.lower())
            ttt_follow = list(dict.fromkeys(ttt_follow))

            try:
                ttt_follow = get_a_better_list(t_follow)
            except:
                pass
            
                        
            for i in range(len(ttt_follow)):
                if ttt_follow[i] != "" and ttt_follow[i].lower() not in tttt_follow:
                    if ttt_follow[i].lower().replace("@","") not in tttt_follow:
                        tttt_follow.append(ttt_follow[i])
                
            
            alph_list = int(len(tttt_follow)/2)

            for i in range(alph_list):
                follow_nbr +=1
                print("Account n " + str(follow_nbr) + " / " + str(len(tttt_follow)) + " account name: " + tttt_follow[i])
                follow_an_account(S,tttt_follow[i],2)
                alph_follow.append(tttt_follow[i].lower())

            if len(tttt_follow) > 80:
                time.sleep(120)

            for t in tweet_from_url:
                print("Giveaway number " + str(giveaway_g) + " / " + str(len(tweet_from_url)) + " all giveaway (even the one already done) " + str(giveaway_done))
                like = like_a_tweet(S,t)
                time.sleep(S.wait_time)    
                if like == True:
                    giveaway_done  += 1
                    giveaway_g += 1
                    reetweet_a_tweet(S,t)
                    #time.sleep(S.wait_time)        
                    try:       
                        if t_comment_or_not[idxx] == True:
                            comment_a_tweet(S,t,t_full_comment[idxx])
                        time.sleep(randint(MINTIME,MAXTIME))
                    except:
                        print("An error happend skiping this comment")
                else:
                    giveaway_done  += 1
                    print("You have already like the tweet")
                    time.sleep(2)
                if giveaway_g % 10 == 0 and giveaway_g > 1 and human == True:
                    time.sleep(5400)
                print(idxx)
                idxx = idxx + 1
            
            for account_to_follow in tttt_follow:
                print("Account n " + str(follow_nbr) + " / " + str(len(tttt_follow)) + " account name: " + account_to_follow)
                if account_to_follow.lower() not in alph_follow:
                    follow_an_account(S,account_to_follow,2)
                    follow_nbr +=1            
            
            if random_rt_and_tweet == True:
                if random_action == True and random_tweet_nb > 0:
                    random_tweet_nb = randint(1,random_tweet_nb)
                for i in range(random_tweet_nb):
                    info , info_link = get_news()
                    make_a_tweet(S,info+" "+info_link)
                    time.sleep(randint(MINTIME,MAXTIME))
                make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                try:
                    rt_url = search_tweet_for_better_rt(S)
                
                    for i in range(len(rt_url)):
                        like = like_a_tweet(S,rt_url[i])
                        if like == True:            
                            reetweet_a_tweet(S,rt_url[i])
                        time.sleep(randint(MINTIME,MAXTIME))
                except:
                    print("ok")
                
        print("Giveaway finished for this account sleeping a bit")
        giveaway_g = 0
        idxx = 0
        follow_nbr = 0
        giveaway_done = 0
        time.sleep(180)
    print("End of the program")