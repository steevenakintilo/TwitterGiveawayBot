
import yaml
from random import randint
import re
import emoji
import time
import traceback
import random
from datetime import datetime, timedelta, date
import pickle


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class Data:
    with open("configuration.yml", "r",encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    word_to_search = data["words_to_search"]
    accounts_to_tag_ = data["accounts_to_tag"]
    accounts_to_tag_ = random.sample(accounts_to_tag_, len(accounts_to_tag_))
    accounts_to_tag = []
    accounts_to_blacklist = data["accounts_to_blacklist"]
    sentence_for_tag = data["sentence_for_tag"]
    hashtag_to_blacklist = data["hashtag_to_blacklist"]
    giveaway_to_blacklist = data["giveaway_to_blacklist"]
    max_giveaway = data["max_giveaway"]
    minimum_like = data["minimum_like"]
    minimum_rt = data["minimum_rt"]
    maximum_day = data["maximum_day"]
    nb_of_giveaway = data["nb_of_giveaway"]
    sentence_for_random_comment = data["sentence_for_random_comment"]
    tweet_lang = data["tweet_lang"]
    add_sentence_to_tag = data["add_sentence_to_tag"]
    word_list_to_check_for_special_comment = data["word_list_to_check_for_special_comment"]
    word_list_to_check_for_comment = data["word_list_to_check_for_comment"]
    short_word_list_to_check_for_comment = data["short_word_list_to_check_for_comment"]
    word_list_to_check_for_tag = data["word_list_to_check_for_tag"]
    one_poeple_list = data["one_poeple_list"]
    two_poeple_list = data["two_poeple_list"]
    three_or_more_poeple_list = data["three_or_more_poeple_list"]
    four_or_more_poeple_list = data["four_or_more_poeple_list"]
    random_action = data["random_action"]
    add_hashtag_to_comment = data["add_hashtag_to_comment"]
    word_list_to_not_check_for_copy = data["word_list_to_not_check_for_copy"]
    copy = data["copy"]
    tag_more_than_three = data["tag_more_than_three"]
    accounts_to_tag_more = data["accounts_to_tag_more"]


def is_date_older_than_a_number_of_day(date_str):
    d = Data()
    date_str = str(date_str)
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    delta = today - date
    if delta.days > d.maximum_day:
        return True
    else:
        return False

def remove_non_alphanumeric(string):
    s = string.split("\n")
    return s[0]

def write_into_file(path, x):
    with open(path, "ab") as f:
        f.write(str(x).encode("utf-8"))

def reset_file(path):  
    f = open(path, "w")
    f.write("")    
    f.close            

def print_file_info(path):
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return(content)

def remove_emojie(text):
    return emoji.replace_emoji(text, replace='')
    #return emoji.get_emoji_regexp().sub(r'',text)

def delete_hashtag_we_dont_want(l):
    d = Data()
    new_l = []
    for elem in l:
        if elem.lower().replace("#","") not in d.hashtag_to_blacklist and len(new_l) <= 2 and elem not in new_l:
            new_l.append(elem.lower() + " ")
    new_l = list(dict.fromkeys(new_l))
    return (" ".join(new_l))


def check_for_forbidden_word(sentence):
    d = Data()
    forbidden = d.giveaway_to_blacklist
    for elem in forbidden:
        if elem.lower() in sentence.lower():
            return True
    return False

def check_alpha_numeric(string):
    string = string.lower()
    alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_@"
    for elem in string:
        if elem not in alphanumeric:
            return False
    return True

def check_alpha_numeric_pos(string):
    string = string.lower()
    alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789_@"
    for i in range(len(string)):
        if string[i] not in alphanumeric:
            return i
    return 0



def list_of_account_to_follow(maker_of_the_tweet,sentence):
    
    account_to_follow = [maker_of_the_tweet.replace("@","").lower()]
    sentence = str(sentence).replace("\n"," ").replace("\n\n"," ").replace("\n\n\n"," ").replace("\n\n\n\n"," ")
    s = sentence.split()
    for word in s:
        try:
            if word[0] == "@" and word.lower() not in maker_of_the_tweet and word.lower() != maker_of_the_tweet:
                account_to_follow.append(word.replace("@","").lower())
        except:
            pass
    account_to_follow = list(dict.fromkeys(account_to_follow))
    return (" ".join(account_to_follow))

def get_the_right_word(sentence):
    new_sentence = ""
    
    guillemet_counter = 0
    for i in range(len(sentence)):
        if sentence[i] == '"' or sentence[i] == '“' or sentence[i] == '«' or sentence[i] == "»":
            guillemet_counter = guillemet_counter + 1
        if guillemet_counter >= 2:
            break
        if guillemet_counter == 1 or sentence[i] == '"' or sentence[i] == '“' or sentence[i] == "«" or sentence[i] == "»":
            new_sentence = new_sentence + sentence[i]
    
    return (new_sentence.replace('"',"").replace("“","").replace("«","").replace("»",""))

def what_to_comment(sentences,S,url):
    s = sentences.split("\n")
    d = Data()
    special_char = ",;.!?\n"
    forbiden = False
    for word in d.word_list_to_not_check_for_copy:
        if word.lower() in sentences.lower():
            forbiden = True
    
    if forbiden == False:
        for word in d.word_list_to_check_for_special_comment:
            s = sentences.lower()
            if word in sentences.lower():
                next_part = s.split(word)[1]
                if '"' not in next_part and '“' not in next_part and  "«" not in next_part and "”" not in next_part and "»" not in next_part:
                    copied_comment = copy_a_comment(S,url)
                    if copied_comment != False:
                        return copied_comment
    
    for word in d.word_list_to_check_for_special_comment:
        if word in sentences.lower():
            comment = sentences.split(word)
            if len(comment) == 1:
                c = comment[0]
            else:
                c = comment[1]
            if '"' in c or '“' in c or "«" in c:
                c = get_the_right_word(c)
            c = c.lower()
            if "@" in c:
                c = c.split("@")[0]
            if "@" not in c:
                for i in range(len(special_char)):
                    if special_char[i] in c:
                        c = c.split(special_char[i])[0]
                        break
            if "#" in word:
                c = "#" + c
                if "\n" in c:
                    slash = c.split("\n")
                    if len(slash) > 2:
                        return ("")
                return(c.replace('"',"").replace("“","").replace("«","").replace("»","").replace(word,"").replace("”",""))
            if "\n" in c:
                slash = c.split("\n")
                if len(slash) > 2:
                    return ("")
            return(c.replace('"',"").replace("“","").replace("«","").replace("»","").replace(word,"").replace("”",""))

    return ("")

def get_a_better_list(l):
    account_you_follow_from_file = print_file_info("account.txt").split("\n")
    new_l = []
    account = []
    for i in range(len(l)):
        try:
            line_f = l[i].split(" ")
            for j in range(len(line_f)):
                new_l.append(line_f[j])
                if line_f[j].replace(",","").replace(";","").replace("-","") not in account:
                    account.append(line_f[j].replace(",","").replace(";",""))
                    if line_f[j].replace(",","").replace(";","").replace("-","") not in account_you_follow_from_file:
                        write_into_file("account.txt",line_f[j].replace(",","").replace(";","").replace("-","")+"\n")
                try:
                    if "." in line_f[j]:
                        l = line_f[j].split(".")[0]
                        account.append(l.replace(",","").replace(";","").replace("-","").replace("-",""))
                        write_into_file("account.txt",l.replace(",","").replace(";","").replace("-","")+"\n")
                except:
                    pass
        except:
            pass
    return (new_l)

def check_if_we_need_to_comment(text):
    d = Data()

    for elem in d.word_list_to_check_for_comment:
        if elem.lower() in text.lower():
            return True
    
    for word_to_check in d.short_word_list_to_check_for_comment:
        for word in text.split():
            if word.lower().startswith(word_to_check.lower()) and len(word) <= len(word_to_check):
                return True

    text = text.lower()
    return False


def check_if_we_need_to_tag(text):
    d = Data()
    
    if "-tag" in text.lower() or "#tag" in text.lower():
        return True
    
    for elem in d.word_list_to_check_for_tag:
        if elem.lower() in text.lower() and elem.lower() != "tag":
            return True
    
    for word_to_check in d.word_list_to_check_for_tag:
        for word in text.split():
            if (word.lower().startswith(word_to_check.lower()) and "tag" in word.lower()):
                return True
    return False

def delete_url(s):
    s_ = s.split(" ")
    n_s = []
    for i in range(len(s_)):
        if "https" not in s_[i]:
            n_s.append(s_[i])
    n =  " ".join(n_s)
    n = n.strip()

    return(n)

def who_many_people_to_tag(text,accounts_to_tag):
    text = text.replace("\n", " ") 
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return(accounts_to_tag[0])
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return(accounts_to_tag[0]+" "+accounts_to_tag[1])
    
    for three in d.three_or_more_poeple_list:
        if three.lower() in text.lower():
            return(accounts_to_tag[0]+" "+accounts_to_tag[1]+" "+accounts_to_tag[2])
    
    # IF YOU WANT TO DO A FUNCTION THAT CHECK 4 PEOPLE TO TAG DO THIS

    for four in d.four_or_more_poeple_list:
        if four.lower() in text.lower():
            return(accounts_to_tag[0]+" "+accounts_to_tag[1]+" "+accounts_to_tag[2]+" "+accounts_to_tag[3])
    

    if d.tag_more_than_three == True:
        for acc in d.accounts_to_tag_more:
            accounts_to_tag.append(acc)
    return(" ".join(accounts_to_tag))
    
def check_if_we_need_to_tag_two(text):
    text = text.replace("\n", " ") 
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return True
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return True
    
    for other in d.three_or_more_poeple_list:
        if other.lower() in text.lower():
            return True
    return False    

def check_blacklist(account):
    d = Data()
    for backlist_account in d.accounts_to_blacklist:
        if account.lower() == backlist_account.lower().replace("@",""):
            return(True)
    return (False)

def return_only_hashtag(sentence):
    sentence = sentence.split("\n")
    sentence = " ".join(sentence)
    sentence = sentence.split(" ")
    new_l = []
    for s in sentence:
        if len(s) > 1:
            if s[0] == "#":
                new_l.append(s)
    return (new_l)

def remove_double_hashtag(string):
    d = Data()
    if d.add_hashtag_to_comment == False:
        return(" ")
    string = string.split(" ")
    hashtag_list = []
    for s in string:
        if s.lower() not in hashtag_list:
            hashtag_list.append(s.lower())
    return (" ".join(hashtag_list))
def check_if_there_is_enough_rt_to_comment(S,url):
    a = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div"
    try:
        S.driver.get(url)
        element = WebDriverWait(S.driver, 2).until(
        EC.presence_of_element_located((By.XPATH,a)))
        u = S.driver.find_element(By.XPATH,a)
        data = u.text.split()
        new_lst = []
        comment_nb = data[0]
        rt_nb = data[1]
        res = 0

        if len(data) <= 4:
            if "K" in data[0]:
                if "." not in comment_nb:
                    comment_nb = comment_nb + "000"
                else:
                    comment_nb = comment_nb + "00"
                comment_nb = comment_nb.replace("K","").replace("k","")
            if "." in comment_nb:
                comment_nb = comment_nb.replace(".","")

            if "K" in data[1]:
                if "." not in rt_nb:
                    rt_nb = rt_nb + "000"
                else:
                    rt_nb = rt_nb + "00"
                rt_nb = rt_nb.replace("K","").replace("k","")
            if "." in rt_nb:
                rt_nb = rt_nb.replace(".","")
            comment_nb = int(comment_nb)
            rt_nb = int(rt_nb)
            
            if int((comment_nb/rt_nb) * 100) >= 33:
                time.sleep(2)
                return False
            else:
                time.sleep(2)
                return True
        else:
            for i in range(len(data)):
                if "k" not in data[i].lower():
                    new_lst.append(data[i])
            comment_nb = int(new_lst[0])
            rt_nb = int(new_lst[1])
            if int((comment_nb/rt_nb) * 100) >= 33:
                time.sleep(2)
                return False
            else:
                time.sleep(2)
                return True
    except Exception as e:
        time.sleep(2)
        return False


def giweaway_from_url_file(tweets_text,account_list,S):
    try:
        d = Data()
        accounts_to_tag_ = d.accounts_to_tag_
        accounts_to_tag_ = random.sample(accounts_to_tag_, len(accounts_to_tag_))
        accounts_to_tag = []
        if len(accounts_to_tag_) >= 3:
            for i in range(3):
                if i == 0:
                    accounts_to_tag.append(" " + accounts_to_tag_[i])
                else:
                    accounts_to_tag.append(accounts_to_tag_[i])
        else:
            accounts_to_tag = [' @Twitter ', '@X ', '@ElonMusk ']   
        tweet_from_url = print_file_info("recent_url.txt").split("\n")
        tweet_from_url_ = []
        if len(tweet_from_url) > len(tweets_text):
            for i in range(len(tweets_text)):
                tweet_from_url_.append(tweet_from_url[i])
        else:
            for i in range(len(tweet_from_url)):
                tweet_from_url_.append(tweet_from_url[i])
        tweets_need_to_comment_or_not = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        url_from_file = print_file_info("url.txt").split("\n")
        print_data = False
        idxx = 0
        for t in tweets_text:
            if idxx % 24 == 0:
                time.sleep(6)
            current_url = tweet_from_url_[idxx]
            words = t.split(" ")
            result = return_only_hashtag(t)
            hashtag = delete_hashtag_we_dont_want(result)
            if check_if_we_need_to_tag(t) == True:
                if check_if_we_need_to_comment(t) == True:
                    what_to_cmt = what_to_comment(t,S,current_url)
                    nb_word = what_to_cmt.split()
                    if "#" not in what_to_cmt:
                        full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                    else:
                        full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    if d.add_sentence_to_tag == True and len(nb_word) >= 5:
                        if what_to_cmt == "":
                            if "#" not in what_to_cmt:
                                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                            else:
                                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                        else:
                            if "#" not in what_to_cmt:
                                full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                            else:
                                full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                        
                    x = randint(0,1)
                    if d.random_action == True:
                        if "#" not in what_to_cmt:
                            full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                        else:
                            full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                        if x == 0:
                            if what_to_cmt == "":
                                if "#" not in what_to_cmt:
                                    full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                                else:
                                    full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                            else:
                                if "#" not in what_to_cmt:
                                    full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " " + remove_double_hashtag(hashtag)
                                else:
                                    full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                else:
                    what_to_cmt = what_to_comment(t,S,current_url)
                    nb_word = what_to_cmt.split()
                    full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    if what_to_cmt == "":
                        if d.add_sentence_to_tag == True and len(nb_word) >= 5:
                            full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    else:
                        if d.add_sentence_to_tag == True and len(nb_word) >= 5:
                            full_phrase = " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    x = randint(0,1)
                    if what_to_cmt == "":
                        if d.random_action == True:
                            full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                            if x == 0:
                                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    else:
                        if d.random_action == True:
                            full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
                            if x == 0:
                                full_phrase = delete_url(what_to_cmt) + who_many_people_to_tag(t,accounts_to_tag) + " "
            else:
                what_to_cmt = what_to_comment(t,S,current_url)
                if delete_url(what_to_cmt) == "":
                    if "#" not in what_to_cmt:
                        full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_cmt) + " " + remove_double_hashtag(hashtag)
                    else:
                        full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_cmt) + " "
                else:
                    if "#" not in what_to_cmt:
                        full_phrase = delete_url(what_to_cmt) + " " + remove_double_hashtag(hashtag)
                    else:
                        full_phrase = delete_url(what_to_cmt) + " "
            if check_if_we_need_to_tag(t) == True or check_if_we_need_to_tag_two(t) == True:
                tweets_need_to_comment_or_not.append(True)
            else:
                if check_if_we_need_to_comment(t) == True:
                    if check_if_there_is_enough_rt_to_comment(S,current_url) == False:
                        tweets_need_to_comment_or_not.append(True)
                    else:
                        tweets_need_to_comment_or_not.append(False)
                else:
                    tweets_need_to_comment_or_not.append(False)    
            tweets_full_comment.append(remove_emojie(remove_double_hashtag(full_phrase)).replace('"',"").replace("“","").replace("«","").replace("»","").replace("”",""))
            try:
                maker_of_the_tweet = current_url.replace("//","").split("/")[1]
            except:
                maker_of_the_tweet = "x"
            tweets_account_to_follow.append(list_of_account_to_follow(maker_of_the_tweet ,t))
            idxx+=1
        for a in account_list:
            if a not in tweets_account_to_follow and a != "f":
                tweets_account_to_follow.append(a)
        
        if print_data == True:
            print(tweets_full_comment)
            #print(tweets_need_to_comment_or_not)
        print(tweets_need_to_comment_or_not)
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)
    except Exception as e:
        print("YOLO YOLO BANG BANG")
        print("Error " + str(e))
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)


def check_elem_on_a_list(elem_, list_):
    return next((l for l in list_ if elem_ in l.lower()), elem_)

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

def get_list_of_comment_of_a_tweet(selenium_session,url,nb_of_comment=10):
    try:
        start_time = time.time()  # Start the timer
        nb = 0
        if nb_of_comment > 0:
            nb_of_comment = nb_of_comment + 1
        selenium_session.driver.get(url)
        time.sleep(1)
        run  = True
        selenium_data = []
        list_of_comment_url = []
        list_of_tweet_url_ = []
        list_len = []
        data_list = []
        text_list = []
        tweet_info_dict = {"username":"",
        "text":""}
        
        p = '"'
        account = ""
        list_len = []
        if nb_of_comment > 50:
            nb_of_comment = 50

        timeout = 120
        
        while run:
            try:
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    print("Timeout reached. Exiting search.")
                    return data_list
                
                element = WebDriverWait(selenium_session.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
                tweets_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
                tweets_username = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="User-Name"]')
                tweets_text = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                last_tweet = tweets_info[len(tweets_info) - 1]
                for tweet_info, tweet_username, tweet_text in zip(tweets_info, tweets_username,tweets_text):
                    if are_last_x_elements_same(list_len,200) == True:
                        run = False
                    list_len.append(len(data_list))
                    if tweet_info not in selenium_data:
                        try:
                            account = str(str(tweet_username.text).split("\n")[1]).replace("@","")
                            account = str(account).lower()
                            lower_data = str(tweet_info.get_property('outerHTML')).lower()
                            
                            text_ = tweet_text.text.replace("Show more","")
                            if "@" in text_:
                                get_text = str(tweet_info.get_property('outerHTML')).lower().split("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
                                get_text = get_text[4].split("<")
                                get_text = get_text[0].replace("\n"," ")
                                get_text = get_text[2:len(get_text)]
                                text_list = [text.text.replace("\n"," ").lower() for text in tweets_text]
                                text_ = check_elem_on_a_list(get_text,text_list)
                            
                            splinter = "href="+p+"/"+account+"/status"
                            splinter = splinter.replace("\\","/")                    
                            lower_data = lower_data.split(splinter)
                            lower_data = str(lower_data[1])
                            lower_data = lower_data.split(" ")
                            tweet_id = lower_data[0].replace("/","").replace(p,"")
                            tweet_link = "https://x.com/" + account + "/status/" + tweet_id
                            ussr = str(url.split("https://x.com/")[1]).split("/")[0]
                            if "photo1" in tweet_link and "/photo" not in tweet_link:
                                tweet_link = tweet_link.replace("photo1","/photo1")
                            if tweet_link not in list_of_comment_url:
                                if tweet_link[len(tweet_link) - 1] in "0123456789" and "status" in tweet_link:
                                    if account.lower() != ussr.lower():
                                        tweet_info_dict = {"username":account,"text":text_,"url":tweet_link}
                                        data_list.append(tweet_info_dict)
                            if account.lower() != ussr.lower():
                                selenium_data.append(tweet_info)
                            selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                            time.sleep(0.025)
                        except:
                            selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                            time.sleep(0.1)
                        
                        if len(data_list) >= nb_of_comment:
                            run = False
                            return(data_list)
                if len(data_list) > 0:
                    data_list = data_list[1:]
                if len(data_list) > nb_of_comment:
                    for i in range(0,nb_of_comment):
                        list_of_tweet_url_.append(data_list[i])
                
                    return(list_of_tweet_url_)
        
            except Exception as e:
                return (data_list)
        return(data_list)
    except Exception as e:
        return (False)

def copy_a_comment(selenium_session,url):
    try:
        d = Data()
        if d.copy == False:
            return False
        list_of_comment_of_a_tweet = get_list_of_comment_of_a_tweet(selenium_session,url,20)
        if list_of_comment_of_a_tweet == False:
            return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])
        list_of_text = []
        final_list = []
        last_list = []
        if len(list_of_comment_of_a_tweet) == 0:
            quit()
        for l in list_of_comment_of_a_tweet:
           if "text-overflow:" not in l["text"]:
                if "@" in l["text"]:
                    result = re.sub(r'@\w+\s*', '', l["text"])
                    list_of_text.append(result)
                else:
                    list_of_text.append(l["text"])
        
        nb_nbr , nb_hashtag = 0 , 0
        nb = False
        hashtag = False
        single = 0
        d = Data()
        for t in list_of_text:
            if any(char.isdigit() for char in t):
                nb_nbr+=1
            if "#" in t:
                nb_hashtag+=1
        if nb_nbr >= int((len(list_of_text)/3)*2) and len(list_of_text) >= 5:
            nb = True
        
        if nb_hashtag >= int((len(list_of_text)/3)*2) and len(list_of_text) >= 5:
            hashtag = True
        
        for t in list_of_text:
            z = remove_emojie(t)
            if nb == True and hashtag == True and len(z) >= 1 and len(z) <= 150 and any(char.isdigit() for char in t) and "#" in z:
                final_list.append(z)
            elif nb == True and hashtag == False and len(z) >= 1 and len(z) <= 150 and any(char.isdigit() for char in t):
                final_list.append(z)
            elif nb == False and hashtag == True and len(z) >= 1 and len(z) <= 150 and "#" in z:
                final_list.append(z)
            elif len(z) >= 1 and len(z) <= 150 and nb == False and hashtag == False:
                final_list.append(t)
               
        for t in final_list:
            if len(t.split()) <= 3:
                single+=1
        
        average_sentence_lenght = 0
        
        for elem in final_list:
            average_sentence_lenght+=len(elem)
        average_sentence_lenght = int(average_sentence_lenght/len(final_list))
        if average_sentence_lenght > 90:
            return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])
        
        for elem in final_list:
            if len(elem.split()) <= 3:
                last_list.append(elem.lower())
        if (single >= int((len(list_of_text)/3)) or hashtag == True) and len(last_list) > 0 and average_sentence_lenght < 75:
            return (last_list[randint(0,len(last_list) - 1)].replace("\n"," ") + " ")
        else:
            return (final_list[randint(0,len(final_list) - 1)].replace("\n"," ") + " ")
            
    except:
        d = Data()
        return (d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)])