
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import pickle

from selenium.webdriver.common.by import By
from get_tweet import *
import traceback
import feedparser
from random import randint


class Scraper:
    wait_time = 5
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)  # to open the chromedriver    
    #options = webdriver.FirefoxOptions()
    #options.headless = False

    #driver = webdriver.Firefox(options=options)

    username_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
    
    button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
    password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div'
    like_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[3]/div'
    test_tweet = 'https://twitter.com/Twitter/status/1580661436132757506'
    cookie_button_xpath = '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div/span/span'
    notification_button_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span/span'
    reetweet_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[2]/div'
    reetweet_confirm_button_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/span'
    comment_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[1]/div'
    textbox_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
    follow_button_xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div"
    
def get_news():
    url_list = ["https://www.france24.com/fr/rss",
    "https://www.france24.com/fr/europe/rss",
    "https://www.france24.com/fr/france/rss",
    "https://www.france24.com/fr/afrique/rss",
    "https://www.france24.com/fr/moyen-orient/rss",
    "https://www.france24.com/fr/am%C3%A9riques/rss",
    "https://www.france24.com/fr/asie-pacifique/rss",
    "https://www.france24.com/fr/%C3%A9co-tech/rss",
    "https://www.france24.com/fr/sports/rss",
    "https://www.france24.com/fr/culture/rss",
    "https://www.france24.com/fr/plan%C3%A8te/rss",
    ]

    l = url_list[randint(0,len(url_list) - 1)]
    #l = "https://www.france24.com/fr/rss"
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
        print(news_title[rdm_news],news_link[rdm_news])
    except:
        try:
            return(news_title[0],news_link[0])
            print(news_title[0],news_link[0])
        except:
            return ("ok","ok")
            print("ok","ok")

def login(S,_username,_password):

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

    #print("Closing Twitter")


def accept_coockie(S):
    try:
        S.driver.get(S.test_tweet)

        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.cookie_button_xpath)))
        
        cookie_button = S.driver.find_element(By.XPATH,S.cookie_button_xpath)
        cookie_button.click()

    except:
        print("error")
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
        print("error")
        pass    
    
    print("notification done")
    
    
def like_a_tweet(S,url):

    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.like_button_xpath)))
        
        like_button = S.driver.find_element(By.XPATH,S.like_button_xpath)
        #time.sleep(3000)
        # check the "aria-pressed" attribute
        
        liked_or_not = like_button.get_attribute("aria-label")

        time.sleep(1)

        if liked_or_not.lower() == "like" or liked_or_not.lower() == "aimer":
            like_button.click()
            return True
        if liked_or_not.lower() == "liked" or liked_or_not.lower() == "aimé":
            return False
    except:
        print("Bref like")
        return True

def reetweet_a_tweet(S,url):

    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.reetweet_button_xpath)))
        
        reetweet_button = S.driver.find_element(By.XPATH,S.reetweet_button_xpath)
        reetweet_button.click()

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.reetweet_confirm_button_xpath)))
        
        reetweet_button = S.driver.find_element(By.XPATH,S.reetweet_confirm_button_xpath)
        reetweet_button.click()
        
        print("reetweet done")
    except:
        print("Bref rt")


def comment_a_tweet(S,url,text):

    try:

        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.comment_button_xpath)))
        
        comment_button = S.driver.find_element(By.XPATH,S.comment_button_xpath)
        comment_button.click()

        #print("coment part one")
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.textbox_xpath)))
        
        textbox = S.driver.find_element(By.XPATH,S.textbox_xpath)
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
    
    S.driver.get("https://twitter.com/"+account)
    element = WebDriverWait(S.driver, 30).until(
    EC.presence_of_element_located((By.XPATH, S.follow_button_xpath)))
    
    follow_button = S.driver.find_element(By.XPATH,S.follow_button_xpath)

    time.sleep(1)

    aria_label = element.get_attribute("aria-label")
    print(aria_label)
    aria_label = aria_label.split(" ")
    follow_or_not = aria_label[0]

    if follow_or_not.lower() == "following" or follow_or_not.lower() == "abonné":
        follow_button.click()
    print("You've unfollowed another account")


def follow_an_account(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.follow_button_xpath)))
        
        follow_button = S.driver.find_element(By.XPATH,S.follow_button_xpath)

        time.sleep(1)

        aria_label = element.get_attribute("aria-label")
        aria_label = aria_label.split(" ")
        
        try:
            follow_or_not = aria_label[0]

            if follow_or_not.lower() == "follow" or follow_or_not.lower() == "suivre":
                follow_button.click()
                time.sleep(60)
                print("You've followed another account " + account)
        except:
            print("You already follow the account")
            pass
    except:
        follow_an_account_error(S,account)


def follow_an_account_error(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")))
        
        follow_button = S.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")

        time.sleep(1)

        aria_label = element.get_attribute("aria-label")
        aria_label = aria_label.split(" ")
        try:
            follow_or_not = aria_label[0]

            if follow_or_not.lower() == "follow" or follow_or_not.lower() == "suivre":
                follow_button.click()
                time.sleep(60)
                print("You've followed another account " + account)
        except:
            print("You already follow the account")
            pass
    except:
        print("Bref follow") 

def main_one():
    print("Inside main one")
    giveaway_done = 0
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    print("Starting the program")
    print("Searching for Giveaway")
    username_info = data["account_username"]
    password_info = data["account_password"]
    sentence_to_tweet = data["setence_to_tweet"]

    tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not = search_giveaway()
    
    for i in range(len(username_info)):
        print("Connecting to " + str(username_info[i]))
        time.sleep(1)
        S = Scraper()
        login(S,username_info[i],password_info[i])
        time.sleep(3)   
        accept_coockie(S)
        time.sleep(S.wait_time)    
        accept_notification(S)
        time.sleep(S.wait_time)
        accept_coockie(S)
        time.sleep(S.wait_time)
        giveaway_g = 0
        follow_nbr = 0
        for i in range(len(tweets_url)):
            print("Giveaway number " + str(giveaway_g) + " / " + str(len(tweets_url)) + " all giveaway (even the one already done) " + str(giveaway_done))
            like = like_a_tweet(S,tweets_url[i])
            time.sleep(S.wait_time)    
            
            if like == True:
                giveaway_done  += 1
                giveaway_g += 1
                reetweet_a_tweet(S,tweets_url[i])
                time.sleep(S.wait_time)        
                if tweets_need_to_comment_or_not[i] == True:
                    comment_a_tweet(S,tweets_url[i],tweets_full_comment[i])
                    time.sleep(45)
            else:
                giveaway_done  += 1
                print("You have already like the tweet")
                time.sleep(5)

        for account_to_follow in tweets_account_to_follow:
            follow_nbr +=1
            print("Account n " + str(follow_nbr) + " / " + str(len(tweets_account_to_follow)) + " account name: " + account_to_follow)
            follow_an_account(S,account_to_follow)
        for i in range(3):
            info , info_link = get_news()
            make_a_tweet(S,info+" "+info_link)
            time.sleep(60)
        make_a_tweet(S,sentence_to_tweet[len(sentence_to_tweet) - 1])
        print("Giveaway finished for this account sleeping a bit")
        giveaway_g = 0
        follow_nbr = 0
        giveaway_done = 0
        time.sleep(180)
    print("End of the program")


def main_two():
    print("Inside main two")
    giveaway_done = 0
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    print("Starting the program")
    print("Searching for Giveaway")
    username_info = data["account_username"]
    password_info = data["account_password"]
    sentence_to_tweet = data["setence_to_tweet"]
    tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not = search_giveaway()
    
    for i in range(len(username_info)):

        print("Connecting to " + str(username_info[i]))
        time.sleep(1)
        S = Scraper()
        login(S,username_info[i],password_info[i])
        time.sleep(3)   
        accept_coockie(S)
        time.sleep(S.wait_time)    
        accept_notification(S)
        time.sleep(S.wait_time)
        accept_coockie(S)
        time.sleep(S.wait_time)
        giveaway_g = 0
        follow_nbr = 0
        for i in range(len(tweets_url)):
            print("Giveaway number " + str(giveaway_g) + " / " + str(len(tweets_url)) + " all giveaway (even the one already done) " + str(giveaway_done))
            like = like_a_tweet(S,tweets_url[i])
            time.sleep(S.wait_time)    
            
            if like == True:
                giveaway_done  += 1
                giveaway_g += 1
                reetweet_a_tweet(S,tweets_url[i])
                time.sleep(S.wait_time)        
                if tweets_need_to_comment_or_not[i] == True:
                    comment_a_tweet(S,tweets_url[i],tweets_full_comment[i])
                    time.sleep(45)
            else:
                giveaway_done  += 1
                print("You have already like the tweet")
                time.sleep(5)

        for account_to_follow in tweets_account_to_follow:
            follow_nbr +=1
            print("Account n " + str(follow_nbr) + " / " + str(len(tweets_account_to_follow)) + " account name: " + account_to_follow)
            follow_an_account(S,account_to_follow)
    
        for i in range(3):
            info , info_link = get_news()
            make_a_tweet(S,info+" "+info_link)
            time.sleep(60)
        make_a_tweet(S,sentence_to_tweet[len(sentence_to_tweet) - 1])
    print("End of the program")
