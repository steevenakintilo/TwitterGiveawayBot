from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta
from get_tweet import *

import os
import traceback
import time

def remove_days(days_to_remove):
    if days_to_remove < 0:
        days_to_remove = 0
    
    date_format = "%Y-%m-%d"
    today_date = datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.strptime(today_date, date_format)
    new_date = current_date - timedelta(days=days_to_remove)
    
    return(new_date.strftime(date_format))


def get_trend(selenium_session):
    try:
      selenium_session.driver.implicitly_wait(15)
      selenium_session.driver.get("https://x.com/explore")
      element = WebDriverWait(selenium_session.driver, 15).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="trend"]')))
      trends = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="trend"]')
      trends_list = []
      pos = 0
      for i in range(len(trends)):
          r = trends[i]
          trends_list.append(r.text.split("\n")[1])
      return(trends_list)
    except Exception as e:
        print("Bref trend")
        return ("a")

def parse_number(num):
    num = str(num)
    if "B" in num:
        if "." in num:
            num  = num.replace(".","").replace("B","")
            num  = num + "00000000"
            
        else:
            num = num.replace("B","")
            num  = num + "000000000"
            
    elif "M" in num:
        if "." in num:
            num  = num.replace(".","").replace("M","")
            num  = num + "00000"

        else:
            num = num.replace("B","")
            num  = num + "000000"
    
    elif "K" in num:
        if "." in num:
            num  = num.replace(".","").replace("K","")
            num = num + "00"
        else:
            num = num.replace("K","")
            num = num + "000"
    else:
        if "." in num:
            num  = num.replace(".","")
    
    if "," in num:
        num = num.replace(",","")
    
    return int(num)

def convert_string_to_date(date_string):
    original_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    new_date = original_date + timedelta(hours=2)
    return (new_date)

def are_last_x_elements_same(lst,x):
    lst_2 = []
    if len(lst) < x:
        return False
    if len(lst) >= x:
        lst.reverse()
        for i in range(0,x):
            l = lst[i]
            if l not in lst_2 and len(lst_2) != 0:
                return False
            else:
                lst_2.append(l)
    return True

def check_elem_on_a_list(elem_, list_):
    return next((l for l in list_ if elem_ in l.lower()), elem_)


def search_tweet(selenium_session,query="hello",nb_of_tweet_to_search=10):
    list_of_tweet_url = []
    selenium_data = []
    list_of_tweet_url_ = []
    list_len = []
    data_list = []
    text_list = []    
    tweet_info_dict = {"username":"",
    "text":"",
    "id":0,
    "url":"",
    "date":"",
    "like":0,
    "retweet":0,
    "reply":0,}
    p = '"'
    nb = 0
    try:
        selenium_session.driver.get("https://x.com/explore")
        run  = True
        p = '"'
        time.sleep(1)
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')))
        input_box = selenium_session.driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')
        input_box.click()
        input_box.send_keys(query)
        input_box.send_keys(Keys.ENTER)
        time.sleep(5)
        while run:
            element = WebDriverWait(selenium_session.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
            tweets_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            tweets_text = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            last_tweet = tweets_info[len(tweets_info) - 1]
            for tweet_info, tweet_text in zip(tweets_info, tweets_text):
                if len(data_list) >= nb_of_tweet_to_search:
                    run = False
                list_len.append(len(data_list))
                if are_last_x_elements_same(list_len,250) == True:
                    run = False
                if tweet_info not in selenium_data:
                    try:
                        lower_data = str(tweet_info.get_property('outerHTML')).lower()
                        splinter = "href=" + p + "/"
                        
                        lower_data = lower_data.split(splinter)
                        user = lower_data[4]
                        user = user.split(p)
                        tweet_stuff = user[0]
                        tweet_link = "https://x.com/" + tweet_stuff
                        user = tweet_stuff.split("/")[0]
                        tweet_link = tweet_link.replace("/analytics","")
                        text_ = "o"
                        if "/status" in tweet_link:
                            get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                            tweet_info_dict = {"username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                            data_list.append(tweet_info_dict)
                            #print("list len ", len(list_of_tweet_url))
                        selenium_data.append(tweet_info)
                        selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                        time.sleep(0.030)
                    except:
                        try:
                            lower_data = str(tweet_info.get_property('outerHTML')).lower()
                            splinter = "href=" + p + "/"
                            lower_data = lower_data.split(splinter)
                            user = lower_data[5]
                            user = user.split(p)
                            tweet_stuff = user[0]
                            tweet_link = "https://x.com/" + tweet_stuff
                            user = tweet_stuff.split("/")[0]
                            text_ = "o"
                            if tweet_link[len(tweet_link) - 1] in "0123456789" and "status" in tweet_link:
                                get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                                tweet_info_dict = {"username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                                data_list.append(tweet_info_dict)
                                list_of_tweet_url.append(tweet_link)
                            
                            selenium_data.append(tweet_info)                        
                            selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                            time.sleep(0.030)
                        except Exception as e:
                            time.sleep(0.1)

        if len(data_list) > nb_of_tweet_to_search:
            for i in range(0,nb_of_tweet_to_search):
                list_of_tweet_url_.append(data_list[i])
            return(list_of_tweet_url_)

        else:
            return (data_list)
    except Exception as e:
        print("Error searching " + query + " tweet")
        return(data_list)
     
def search_tweet_for_better_rt(selenium_session):
    d = Data()
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    nb = data["random_retweet_nb"]
    random_action = data["random_action"]
    word_to_rt = data["word_to_rt"]
    rt_your_word = data["rt_your_word"]
    rt_to_blacklist = data["rt_to_blacklist"]
    blacklist = False
    tweet_found_ = []
    url_list = []
    if random_action == True and nb > 0:
        nb = randint(1,nb)
    
    if random_action == False:
        if rt_your_word == False:
            
            tweet_found = search_tweet(selenium_session,str(get_trend(selenium_session)[0]),nb)
            if d.tweet_lang != "any":
                tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(get_trend(selenium_session)[0]),nb)
            for tweet in tweet_found:
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False
        else:
            tweet_found = search_tweet(selenium_session,str(word_to_rt[randint(0,len(word_to_rt) - 1)]),nb)
            if d.tweet_lang != "any":
                tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(word_to_rt[randint(0,len(word_to_rt) - 1)]),nb)
            for tweet in tweet_found:
                #print(tweet["text"] , tweet["url"])
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False

    else:
        try:
            trend = get_trend(selenium_session)
            trend.append("a")
            if word_to_rt == True:
                trend = word_to_rt
                if len(trend) == 0:
                    trend = get_trend(selenium_session)
                    trend.append("a")
                print("hello")   
            for i in range(nb):
                tweet_found = search_tweet(selenium_session,str(trend[randint(0,len(trend) - 1)]),1)
                if d.tweet_lang != "any":
                    tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(trend[randint(0,len(trend) - 1)]),1)
                for t in tweet_found:
                    if t["url"] not in url_list:
                        for r in rt_to_blacklist:
                            if r in tweet["url"]:
                                blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False
            
            #url_list = []
            #for tweet in tweet_found_:
            #    url_list.append(tweet)
        except:
            tweet_found = search_tweet(selenium_session,str(get_trend(selenium_session)[0]),nb)
            if d.tweet_lang != "any":
                tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(get_trend(selenium_session)[0]),nb)
            for tweet in tweet_found:
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False
    
    return url_list

def list_inside_text(list_one,text):
    for l in list_one:
        if l.lower() not in text.lower():
            return False
    return True

def get_giveaway_url(selenium_session):
    try:
        d = Data()
        reset_file("recent_url.txt")
        tweets_need_to_comment_or_not = []
        tweets_text = []
        tweets_id = []
        tweets_url = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        doublon = 0
        url_from_file = print_file_info("url.txt").split("\n")
        print_data = False
        date_ = ""
        date_format = "%Y-%m-%d"
        check_ = []
        MAX = 250
        giveaway_foud_per_word = 0
        ban_word = ""
        ban_word_list = []
        duplicated_url = []
        for banned_word in d.giveaway_to_blacklist:
            if "." not in banned_word:
                ban_word += "-" + banned_word + " "

        if len(ban_word) <= len(d.giveaway_to_blacklist):
            ban_word = ""
        nb_of_tweet_to_search = d.max_giveaway
        if nb_of_tweet_to_search > 1000:
            nb_of_tweet_to_search = 1000
        if d.nb_of_giveaway > MAX:
            d.nb_of_giveaway = MAX
        for search_word in d.word_to_search:
            if print_data == False:
                print("### " , search_word)
                print("### nb of giveaway foud " , nb_of_giveaway_found)
            if nb_of_giveaway_found <d.nb_of_giveaway and "." not in search_word:
                text = search_word + ' lang:'+d.tweet_lang + " min_faves:"+str(d.minimum_like) + " min_retweets:"+str(d.minimum_rt)+" since:"+str(remove_days(d.maximum_day)) + " " + ban_word
                if d.tweet_lang == "any":
                    text = search_word + " min_faves:"+str(d.minimum_like) + " min_retweets:"+str(d.minimum_rt)+" since:"+str(remove_days(d.maximum_day)) + " " + ban_word
                
                giveaway = search_tweet(selenium_session,text,nb_of_tweet_to_search)
                for g in giveaway:
                    giveaway_foud_per_word+=1
                if nb_of_tweet_to_search < 10:
                    time.sleep(10)
                if nb_of_tweet_to_search <= 100 and nb_of_tweet_to_search >= 10:
                    time.sleep(120)
                if nb_of_tweet_to_search > 100 and nb_of_tweet_to_search <= 300:
                    time.sleep(180)
                if nb_of_tweet_to_search > 300 and nb_of_tweet_to_search <= 999:
                    time.sleep(300)
                if nb_of_tweet_to_search >= 1000:
                    time.sleep(800)
                
                for g in giveaway:
                    if g["url"] not in tweets_url and check_for_forbidden_word(g["text"].lower()) == False and check_blacklist(g["username"]) == False and g["url"] not in url_from_file and nb_of_giveaway_found < d.nb_of_giveaway and check_for_forbidden_word(g["username"].lower()) == False:
                        if nb_of_giveaway_found>=d.nb_of_giveaway:
                            break
                        tweets_url.append(g["url"])
                        nb_of_giveaway_found+=1
                    elif list_inside_text(search_word.split(" "), g["text"]) == False and g["url"] not in url_from_file and g["url"] not in tweets_url and g["url"] not in duplicated_url and check_blacklist(g["username"]) == False:
                        if nb_of_giveaway_found>=d.nb_of_giveaway:
                            break
                        tweets_url.append(g["url"])
                        nb_of_giveaway_found+=1
                        duplicated_url.append(g["url"])
                    else:
                        doublon +=1

                    if nb_of_giveaway_found>=d.nb_of_giveaway:
                        break
            giveaway_foud_per_word = 0
        if len(tweets_id) > d.nb_of_giveaway:
            dif = len(tweets_id) - d.nb_of_giveaway
            tweets_url = tweets_url[:dif]
            
        for url in tweets_url:
            write_into_file("url.txt",url+"\n")
            write_into_file("recent_url.txt",url+"\n")
                    
        tweets_account_to_follow = get_a_better_list(tweets_account_to_follow)
        if print_data == True:
            print(tweets_url)
            print("Nb of doublon " + str(doublon))
        print("Number of giveaway found = " + str(nb_of_giveaway_found))
        if nb_of_giveaway_found > 0:
            print("Ending giveaway search the bot will now start doing giveaways")
        return (tweets_url)    
    except Exception as e:
        print("Error occured but we are still doing some giveaways")
        #traceback.print_exc()
        return (tweets_url)