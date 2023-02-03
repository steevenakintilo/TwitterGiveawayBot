import snscrape.modules.twitter as sntwitter
import yaml
from random import randint


class Data:
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    word_to_search = data["words_to_search"]
    accounts_to_tag = data["accounts_to_tag"]
    accounts_to_blacklist = data["accounts_to_blacklist"]
    sentence_for_tag = data["sentence_for_tag"]
    hashtag_to_blacklist = data["hashtag_to_blacklist"]
    giveaway_to_blacklist = data["giveaway_to_blacklist"]
    max_giveaway = data["max_giveaway"]
    minimum_like = data["minimum_like"]


def remove_non_alphanumeric(string):
    s = string.split("\n")
    return s[0]

def write_into_file(path,x):  
    f = open(path, "w")
    f.write(str(x))    
    f.close            

def print_file_info(path):
    f = open(path, 'r')
    content = f.read()
    return(content)
    f.close()


def delete_hashtag_we_dont_want(l):
    d = Data()
    new_l = []

    for elem in l:
        if elem.lower().replace("#","") not in d.hashtag_to_blacklist:
            new_l.append(elem)
    
    return (" ".join(new_l))


def check_for_forbidden_word(sentence):
    d = Data()
    s = sentence.split(" ")
    for word in s:
        if word.lower() in d.giveaway_to_blacklist:
            return True
    return False


def list_of_account_to_follow(maker_of_the_tweet,sentence):
    account_to_follow = [maker_of_the_tweet.replace("@","")]
    s = sentence.split(" ")
    for word in s:
        try:
            if word[0] == "@" and word.replace("@","") != maker_of_the_tweet.replace("@",""):
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

    for sentence in s:
        #comment = ""
        if "commenter" in sentence.lower():
            comment = sentence.split("commenter")
            if len(comment) == 1:
                c = comment[0]
            else:
                c = comment[1]
            if '"' in c or '“' in c:
                c = get_the_right_word(c)
            return(c.replace('"',"").replace("“","").replace("«","").replace("»",""))
            
        if "commente" in sentence.lower():
            comment = sentence.split("commente")
            if len(comment) == 1:
                c = comment[0]
            else:
                c = comment[1]
            if '"' in c or '“' in c:
                c = get_the_right_word(c)
            return(c.replace('"',"").replace("“","").replace("«","").replace("»",""))

        if "écrit" in sentence.lower():
            comment = sentence.split("écrit")
            if len(comment) == 1:
                c = comment[0]
            else:
                c = comment[1]
            if '"' in c or '“' in c:
                c = get_the_right_word(c)
            return(c.replace('"',"").replace("“","").replace("«","").replace("»",""))
            
        if "écrire" in sentence.lower():
            comment = sentence.split("écrire")
            if len(comment) == 1:
                c = comment[0]
            else:
                c = comment[1]
            if '"' in c or '“' in c:
                c = get_the_right_word(c)
            return(str(c.replace('"',"").replace("“","").replace("«","").replace("»","")))
        
    return ("")
                
def search_giveaway():
    d = Data()
    tweets_text = []
    tweets_id = []
    tweets_url = []
    tweets_full_comment = []
    tweets_account_to_follow = []
    nb_of_giveaway_found = 0
    char = '#'
    full_phrase = ""
    doublon = 0
    for search_word in d.word_to_search:
        text = search_word + ' lang:fr'
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(text).get_items()):
            if tweet.id not in tweets_id and tweet.likeCount >= d.minimum_like and check_for_forbidden_word(tweet.content) == False and tweet.username not in d.accounts_to_blacklist:
                url =  f"https://twitter.com/user/status/{tweet.id}"
                words = text.split()
                result = [word for word in words if word.startswith(char)]
                hashtag = delete_hashtag_we_dont_want(result)
                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + what_to_comment(tweet.content) + " ".join(d.accounts_to_tag) + hashtag
                tweets_id.append(tweet.id)
                tweets_text.append(tweet.content)
                tweets_url.append(url)
                tweets_account_to_follow.append(list_of_account_to_follow(tweet.username ,tweet.content))
                tweets_full_comment.append(full_phrase)
                nb_of_giveaway_found+=1
                #print(tweet.content,url)
                #print(full_phrase)
            else:
                doublon +=1
            if i>d.max_giveaway:
                break
    #print(tweets_text)
    #print(tweets_url)
    #print(tweets_full_comment)
    #print(tweets_account_to_follow)
    #print(" Nb of doublon " + str(doublon))
    print("Nb of giveaway found = " + str(nb_of_giveaway_found))
    return (tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow)
    
search_giveaway()
