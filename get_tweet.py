#import snscrape.modules.twitter as sntwitter

import yaml
from random import randint
import re
import emoji
import time
import traceback
import random
from datetime import datetime, timedelta, date

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
        if elem.lower().replace("#","") not in d.hashtag_to_blacklist:
            new_l.append(elem + " ")
    
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
    
    account_to_follow = [maker_of_the_tweet.replace("@","")]
    s = sentence.split(" ")
    for word in s:
        try:
            if word[0] == "@" and word.replace("@","") != maker_of_the_tweet.replace("@",""):
                if "." in  word:
                    word = word.split(".")[0]
                if "\n" in word:
                    word = word.split("\n")[0]
                if check_alpha_numeric(word) == False:
                    word = word[0:check_alpha_numeric_pos(word) - 1]
                account_to_follow.append(remove_non_alphanumeric(word.replace("@","")))
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

def what_to_comment(sentences):
    s = sentences.split("\n")
    d = Data()
    for word in d.word_list_to_check_for_special_comment:
        for sentence in s:
            if word in sentence.lower():
                comment = sentence.split(word)
                if len(comment) == 1:
                    c = comment[0]
                else:
                    c = comment[1]
                if '"' in c or '“' in c:
                    c = get_the_right_word(c)
                return(c.replace('"',"").replace("“","").replace("«","").replace("»",""))
                
    return ("")

def get_a_better_list(l):
    account_you_follow_from_file = print_file_info("account.txt").split("\n")
    new_l = []
    account = []
    for i in range(len(l)):
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
    return (new_l)

def check_if_we_need_to_comment(text):
    d = Data()

    for elem in d.word_list_to_check_for_comment:
        if elem.lower() in text.lower():
            return True
    
    for word_to_check in d.short_word_list_to_check_for_comment:
        for word in text.split():
            if word.lower().startswith(word_to_check.lower()) and len(word) <= 6:
                return True

    text = text.lower()
    return False


def check_if_we_need_to_tag(text):
    d = Data()
    for elem in d.word_list_to_check_for_tag:
        if elem.lower() in text.lower():
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
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return(accounts_to_tag[0])
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return(accounts_to_tag[0]+" "+accounts_to_tag[1])
    
    return(" ".join(accounts_to_tag))
    
def check_if_we_need_to_tag_two(text):
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
    d = Data
    for backlist_account in d.accounts_to_blacklist:
        if account.lower() == backlist_account.lower().replace("@",""):
            return(True)
    return (False)


# def search_giveaway_not_working_anymore_since_snscrape_is_down_and_i_have_made_my_own_function_who_work_well_too_so_i_keep_this_function_just_in_case_snscrape_will_work_again_and_also_for_the_big_name_of_the_function_which_is_funny_for_me_and_maybe_not_for_everyone():
#     try:
#         d = Data()
#         reset_file("recent_url.txt")
#         tweets_need_to_comment_or_not = []
#         tweets_text = []
#         tweets_id = []
#         tweets_url = []
#         tweets_full_comment = []
#         tweets_account_to_follow = []
#         nb_of_giveaway_found = 0
#         char = '#'
#         full_phrase = ""
#         doublon = 0
#         url_from_file = print_file_info("url.txt").split("\n")
#         print_data = False
#         date_ = ""
#         date_format = "%Y-%m-%d"
#         for search_word in d.word_to_search:
#             text = search_word + ' lang:'+d.tweet_lang
#             if d.tweet_lang == "any":
#                 text = search_word 
#             for i,tweet in enumerate(sntwitter.TwitterSearchScraper(text).get_items()):
#                 date_ = str(tweet.date)
#                 date_ = date_[0:10]
#                 year, month, day = map(int, date_.split("-"))
#                 ddate = date(year, month, day)
#                 url =  f"https://twitter.com/user/status/{tweet.id}"
#                 if tweet.id not in tweets_id and tweet.likeCount >= d.minimum_like and check_for_forbidden_word(tweet.rawContent) == False and check_blacklist(tweet.user.username) == False and url not in url_from_file and is_date_older_than_a_number_of_day(ddate) == False and tweet.retweetCount >= d.minimum_rt and nb_of_giveaway_found < d.nb_of_giveaway:
#                     words = tweet.rawContent.split()
#                     result = [word for word in words if word.startswith(char)]
#                     hashtag = delete_hashtag_we_dont_want(result)
#                     if check_if_we_need_to_tag(tweet.rawContent) == True:
#                         if check_if_we_need_to_comment(tweet.rawContent) == True:
#                             full_phrase = delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " " + hashtag
#                             if d.add_sentence_to_tag == True:
#                                 full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " " + hashtag
#                         else:
#                             full_phrase = delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " "
#                             if d.add_sentence_to_tag == True:
#                                 full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " "
#                     else:
#                         full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + " " + hashtag
#                     tweets_id.append(tweet.id)
#                     tweets_text.append(tweet.rawContent)
#                     tweets_url.append(url)
#                     if check_if_we_need_to_tag(tweet.rawContent) == True or check_if_we_need_to_tag_two(tweet.rawContent) == True:
#                         tweets_need_to_comment_or_not.append(True)
#                     else:
#                         tweets_need_to_comment_or_not.append(check_if_we_need_to_comment(tweet.rawContent))
#                     tweets_account_to_follow.append(list_of_account_to_follow(tweet.user.username ,tweet.rawContent))
#                     tweets_full_comment.append(remove_emojie(full_phrase))
#                     write_into_file("url.txt",url+"\n")
#                     write_into_file("recent_url.txt",url+"\n")
#                     nb_of_giveaway_found+=1
#                 else:
#                     doublon +=1
#                 if nb_of_giveaway_found>=d.nb_of_giveaway:
#                     break
#         tweets_account_to_follow = get_a_better_list(tweets_account_to_follow)
#         if print_data == True:
#             print(tweets_text)
#             print(tweets_url)
#             print(tweets_full_comment)
#             print(tweets_account_to_follow)
#             print("Nb of doublon " + str(doublon))
#         print("Number of giveaway found = " + str(nb_of_giveaway_found))
#         print("Ending giveaway search")
#         return (tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not)
#     except Exception as e:
#         print("SNSCRAPE ERROR")
#         return (tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not)

def giweaway_from_url_file(tweets_text,account_list):
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
        tweets_need_to_comment_or_not = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        url_from_file = print_file_info("url.txt").split("\n")
        print_data = False
        for t in tweets_text:
            words = t.split(" ")
            result = [word for word in words if word.startswith(char)]
            hashtag = delete_hashtag_we_dont_want(result)
            if check_if_we_need_to_tag(t) == True:
                if check_if_we_need_to_comment(t) == True:
                    full_phrase = delete_url(what_to_comment(t)) + who_many_people_to_tag(t,accounts_to_tag) + " " + hashtag
                    if d.add_sentence_to_tag == True:
                        full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(t)) + who_many_people_to_tag(t,accounts_to_tag) + " " + hashtag
                else:
                    full_phrase = delete_url(what_to_comment(t)) + who_many_people_to_tag(t,accounts_to_tag) + " "
                    if d.add_sentence_to_tag == True:
                        full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(t)) + who_many_people_to_tag(t,accounts_to_tag) + " "
            else:
                full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_comment(t)) + " " + hashtag
            
            if check_if_we_need_to_tag(t) == True or check_if_we_need_to_tag_two(t) == True:
                tweets_need_to_comment_or_not.append(True)
            else:
                tweets_need_to_comment_or_not.append(check_if_we_need_to_comment(t))
            tweets_full_comment.append(remove_emojie(full_phrase))
            tweets_account_to_follow.append(list_of_account_to_follow("" ,t))
        for a in account_list:
            if a not in tweets_account_to_follow and a != "f":
                tweets_account_to_follow.append(a)
        if print_data == True:
            print(tweets_full_comment)
            print(tweets_need_to_comment_or_not)
        print(tweets_need_to_comment_or_not)
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)
    except Exception as e:
        print("YOLO YOLO BANG BANG")
        print("Error " + str(e))
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)
