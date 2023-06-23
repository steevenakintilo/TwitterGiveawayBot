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

with open("configuration.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    
MINTIME = data["min_time"]
MAXTIME = data["max_time"]

class Scraper:
    wait_time = 5
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)  # to open the chromedriver    
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
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="like"]')))
        
        like_button = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="like"]')
        #time.sleep(3000)
        # check the "aria-pressed" attribute
        
        liked_or_not = like_button.get_attribute("aria-label")


        if liked_or_not.lower() == "like" or liked_or_not.lower() == "aimer":
            like_button.click()
            return True
        if liked_or_not.lower() == "liked" or liked_or_not.lower() == "aimé":
            return False
    except:
        print("Bref like" * 10)
        return True


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
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="reply"]')))
        
        comment_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
        comment_button.click()

      #  print("coment part one")
        time.sleep(10)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
        
        textbox = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        textbox.click()
        time.sleep(S.wait_time)
        textbox.send_keys(text)
        
     #   print("coment part two")
        time.sleep(15)
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))

        wait = WebDriverWait(S.driver, 10)
        target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))

        S.driver.execute_script("arguments[0].scrollIntoView();", target_element)

        target_element.click()

        time.sleep(20)
    #    print("comment part three")
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
        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.follow_button_xpath)))
        
        follow_button = S.driver.find_element(By.XPATH,S.follow_button_xpath)

        time.sleep(1)

        aria_label = element.get_attribute("aria-label")
        aria_label = aria_label.split(" ")
        
        try:
            follow_or_not = aria_label[0]

            if follow_or_not.lower() != "follow" and follow_or_not.lower() != "suivre":
                follow_button.click()
                element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="confirmationSheetConfirm"]')))
                confirm_click = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="confirmationSheetConfirm"]')
                confirm_click.click()
                S.unfollow_nbr+=1
                time.sleep(15)
                print("You've unfollowed another account " + account)
        except:
            print("You already unfollow the account")
            pass
    except Exception as e:
        print("Bref unfollow " + str(e))
        unfollow_an_account_error(S,account)


def unfollow_an_account_error(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")))
        
        follow_button = S.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")

        time.sleep(1)

        aria_label = element.get_attribute("aria-label")
        aria_label = aria_label.split(" ")
        try:
            follow_or_not = aria_label[0]

            if follow_or_not.lower() != "follow" and follow_or_not.lower() != "suivre":
                follow_button.click()
                element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="confirmationSheetConfirm"]')))
                confirm_click = S.driver.find_element(By.CSS_SELECTOR,'[data-testid="confirmationSheetConfirm"]')
                confirm_click.click()
                S.unfollow_nbr+=1
                time.sleep(15)
                print("You've unfollowed another account " + account)
        except:
            print("You already unfollow the account")
            pass
    except Exception as e:
        print("Bref unfollow " + str(e)) 


def follow_an_account(S,account,t):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, t).until(
        EC.presence_of_element_located((By.XPATH, S.follow_button_xpath)))
        
        follow_button = S.driver.find_element(By.XPATH,S.follow_button_xpath)

        time.sleep(1)

        aria_label = element.get_attribute("aria-label")
        aria_label = aria_label.split(" ")
        
        try:
            follow_or_not = aria_label[0]

            if follow_or_not.lower() == "follow" or follow_or_not.lower() == "suivre":
                follow_button.click()
                element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]")))
                confirm_click = S.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]")
                time.sleep(randint(MINTIME,MAXTIME))
                print("You've followed another account " + account)
        except:
            print("You already follow the account")
            pass
    except:
        follow_an_account_error(S,account,t)


def follow_an_account_error(S,account,t):
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
                time.sleep(randint(MINTIME,MAXTIME))
                print("You've followed another account " + account)
        except:
            print("You already follow the account")
            pass
    except:
        print("Bref follow") 


def get_only_account(s):
    l = []
    for i in range(len(s)):
        if s[i][0] == "@":
            l.append(s[i])
    return (l)

def scroll_down(S,account):
    S.driver.get("https://twitter.com/" + account + "/following")
    
    # Get the current scroll height
    last_height = S.driver.execute_script("return document.body.scrollHeight")
    test = 0
    new_height = 0
    last_height = 0
    # Keep scrolling until the bottom of the page is reached
    element = WebDriverWait(S.driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div")))
    while True:
        S.driver.execute_script("window.scrollBy(0, 500)")        
        test = test + 1
        new_height = S.driver.execute_script("return document.body.scrollHeight")
        print(test)
        time.sleep(0.02)
        if test > 3000:
            break
        last_height = new_height
    
    element = WebDriverWait(S.driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div")))
    account = element.text
    account = account.split("\n")
    return(get_only_account(account))
    

def get_trend(S):
    try:
        S.driver.get("https://twitter.com/explore")
        element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div/div/section/div/div/div[3]/div/div/div/div/div[2]")))
        print(element.text)
        return (str(element.text))
    except:
        print("Bred trend")
        return ("je")

def check_for_unfollow(S,account):
    try:
        S.driver.get("https://twitter.com/"+account)
        element = WebDriverWait(S.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span")))    
        time.sleep(5)
        print("The account currently have " + str(int(element.text.replace(" ",""))) + " following")
        if int(element.text.replace(" ","")) > 4500:
            print("Time to unfollow people") 
            for i in range(10):
                list_of_people_to_unfollow = scroll_down(S,account)
                print(list_of_people_to_unfollow,len(list_of_people_to_unfollow))
                for ac in list_of_people_to_unfollow:
                    unfollow_an_account(S,ac.replace("@",""))
        else:
            print("Don't have to unfollow people")
        print("Nbr of account unfollowed = " + str(S.unfollow_nbr))
    except:
        print("Bref unfollow")

def get_tweet_text(S,url):
    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]')))
        return (str(element.text))
    except:
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


def get_who_to_follow(S,url):

    try:
        a = get_tweet_username(S,url)
        b = get_tweet_text(S,url)
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
    with open("configuration.yml", "r") as file:
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
    idxx = 0
    if crash_or_no == False:
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
        if crash_or_no == True:
            tweet_txt = []
            tweet_username = []
            crash_follow = []
            t_follow = []
            tt_follow = []
            ttt_follow = []
            tttt_follow = []
            tweet_from_url = print_file_info("recent_url.txt").split("\n")
            for t in tweet_from_url:
                tweet_txt.append(get_tweet_text(S,t))
                crash_follow.append(get_tweet_username(S,t))
                for g in get_who_to_follow(S,t):
                    tt_follow.append(g)
            
            
            
            for tt in tt_follow:
                t_follow.append(tt)
            t_comment_or_not , t_full_comment, t_follows = giweaway_from_url_file(tweet_txt,crash_follow)
            
            t_follows.remove("")

            for t in t_follows:
                if t != "":
                    t_follow.append(t.replace(" ",""))
            
            t_follow = list(dict.fromkeys(t_follow))
            for c in t_follow:
                if c.lower() not in ttt_follow:
                    ttt_follow.append(c.lower())
            ttt_follow = list(dict.fromkeys(ttt_follow))
            ttt_follow = get_a_better_list(t_follow)
            
            for i in range(len(ttt_follow)):
                if ttt_follow[i] != "" and ttt_follow[i].lower() not in tttt_follow:
                    tttt_follow.append(ttt_follow[i])
            
            for account_to_follow in tttt_follow:
                follow_nbr +=1
                print("Account n " + str(follow_nbr) + " / " + str(len(tttt_follow)) + " account name: " + account_to_follow)
                follow_an_account(S,account_to_follow,5)
            
            for t in tweet_from_url:
                print("Giveaway number " + str(giveaway_g) + " / " + str(len(tweet_from_url)) + " all giveaway (even the one already done) " + str(giveaway_done))
                like = like_a_tweet(S,t)
                time.sleep(S.wait_time)    
                if like == True:
                    giveaway_done  += 1
                    giveaway_g += 1
                    reetweet_a_tweet(S,t)
                    time.sleep(S.wait_time)        
                    if t_comment_or_not[idxx] == True:
                        comment_a_tweet(S,t,t_full_comment[idxx])
                else:
                    giveaway_done  += 1
                    print("You have already like the tweet")
                    time.sleep(2)
                print(idxx)
                idxx = idxx + 1
            if random_rt_and_tweet == True:
                for i in range(random_tweet_nb):
                    info , info_link = get_news()
                    make_a_tweet(S,info+" "+info_link)
                    time.sleep(randint(MINTIME,MAXTIME))
                make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                try:
                    rt_url = search_tweet_for_rt(get_trend(S),random_retweet_nb)
                
                    for i in range(len(rt_url)):
                        like = like_a_tweet(S,rt_url[i])
                        if like == True:            
                            reetweet_a_tweet(S,rt_url[i])
                        time.sleep(randint(MINTIME,MAXTIME))
                except:
                    print("ok")
            
        if crash_or_no == False:
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
                        time.sleep(randint(MINTIME,MAXTIME))
                else:
                    giveaway_done  += 1
                    print("You have already like the tweet")
                    time.sleep(5)

            for account_to_follow in tweets_account_to_follow:
                follow_nbr +=1
                print("Account n " + str(follow_nbr) + " / " + str(len(tweets_account_to_follow)) + " account name: " + account_to_follow)
                follow_an_account(S,account_to_follow,10)
            if random_rt_and_tweet == True:
                for i in range(random_tweet_nb):
                    info , info_link = get_news()
                    make_a_tweet(S,info+" "+info_link)
                    time.sleep(randint(MINTIME,MAXTIME))
                make_a_tweet(S,sentence_to_tweet[randint(0,len(sentence_to_tweet) - 1)])
                
                rt_url = search_tweet_for_rt(get_trend(S),random_retweet_nb)
                
                for i in range(len(rt_url)):
                    like = like_a_tweet(S,rt_url[i])
                    if like == True:            
                        reetweet_a_tweet(S,rt_url[i])
                    time.sleep(randint(MINTIME,MAXTIME))
                
        print("Giveaway finished for this account sleeping a bit")
        giveaway_g = 0
        idxx = 0
        follow_nbr = 0
        giveaway_done = 0
        time.sleep(180)
    print("End of the program")
