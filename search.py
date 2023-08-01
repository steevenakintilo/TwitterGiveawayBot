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

def get_trend(selenium_session):
    try:
      selenium_session.driver.get("https://twitter.com/explore")
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
        print("Trend error")
        traceback.print_exc()
        return ("je")

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

def search_tweet(selenium_session,query="hello",mode="recent",nb_of_tweet_to_search=10):
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
        if mode == "top":
            selenium_session.driver.get("https://twitter.com/search?q="+query+"&src=typed_query&f=top")
        elif mode == "recent":
            selenium_session.driver.get("https://twitter.com/search?q="+query+"&src=typed_query&f=live")
        else:
            selenium_session.driver.get("https://twitter.com/search?q="+query+"&src=typed_query&f=live")
        
        run  = True
        p = '"'
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
                if are_last_x_elements_same(list_len,500) == True:
                    run = False
                if tweet_info not in selenium_data:
                    try:
                        lower_data = str(tweet_info.get_property('outerHTML')).lower()
                        text_ = tweet_text.text.replace("Show more","")
                        if "@" in text_:
                            get_text = str(tweet_info.get_property('outerHTML')).lower().split("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
                            get_text = get_text[4].split("<")
                            get_text = get_text[0].replace("\n"," ")
                            get_text = get_text[2:len(get_text)]
                            for i in range(len(tweets_text)):
                                try:
                                    text_list.append(tweets_text[i].text)
                                except:
                                    pass
                                
                            text_ = check_elem_on_a_list(get_text,text_list)
                            text_list = []

                        splinter = "href=" + p + "/"
                        
                        lower_data = lower_data.split(splinter)
                        user = lower_data[4]
                        user = user.split(p)
                        tweet_stuff = user[0]
                        tweet_link = "https://twitter.com/" + tweet_stuff
                        user = tweet_stuff.split("/")[0]
                        tweet_link = tweet_link.replace("/analytics","")
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
                            text_ = tweet_text.text.replace("Show more","")
                            text_ = tweet_text.text.replace("Show more","")
                            if "@" in text_:
                                get_text = str(tweet_info.get_property('outerHTML')).lower().split("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
                                get_text = get_text[4].split("<")
                                get_text = get_text[0].replace("\n"," ")
                                get_text = get_text[2:len(get_text)]
                                for i in range(len(tweets_text)):
                                    try:                                    
                                        text_list.append(tweets_text[i].text)
                                    except:
                                        pass
                                    
                                text_ = check_elem_on_a_list(get_text,text_list)
                                text_list = []
                            
                            splinter = "href=" + p + "/"
                            lower_data = lower_data.split(splinter)
                            user = lower_data[5]
                            user = user.split(p)
                            tweet_stuff = user[0]
                            tweet_link = "https://twitter.com/" + tweet_stuff
                            user = tweet_stuff.split("/")[0]
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
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    nb = data["random_retweet_nb"]
    tweet_found = search_tweet(selenium_session,str("lang:fr" + " " + get_trend(selenium_session)[0]),"top",nb)
    url_list = []
    for tweet in tweet_found:
        url_list.append(tweet["url"])
    
    return url_list