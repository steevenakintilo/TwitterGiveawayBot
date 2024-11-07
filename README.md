
# TwitterGiveawayBot

Bot greatly inspired by this one: https://github.com/j4rj4r/BotTwitter

## Requirements
To make the code work you will need to have Python and Pip installed in your computer

Link to download python: https://www.python.org/downloads/

Link to download pip: https://pip.pypa.io/en/stable/installation/

Link to download google chrome: https://www.google.com/intl/fr_fr/chrome/ 


Download all the modules required for the bot to work using this command:

```bash
    pip install -r requirements.txt
```

To start the bot just do

```bash
    python main.py
```

If the bot failed to launch after several try set the headless to false on the configuration.yml and if even after that the bot still don't work just make an issues I will help you make it work / or dm me on my discord: "sangokuhomer"

## Features
- The bot can work in any language
- Unlilke the other bots you can find on github this one don't use api which means that any twitter account you have can be used with this bot
- The bot work with 3 txt files: account.txt url.txt and recent_url.txt , account.txt file list all the account you have followed since using the bot, url.txt file list all the giweaway (their links/urls) you have done sice using the bot and recent_url.txt file list all the giweaway (their links/urls) you have done on the last time you used the bot
- Like Retweet and Comment a tweet link to a giveaway
- Follow all the person asked for the giveaway
- It can @ people when needed, comment with # when needed and make no comment when we don't need to
- The bot can do random tweet and retweet to act more "human"
- The bot can work with 1,2,20 or even 100 accounts you just have to fill the configuration.yml file well
- Unfollow account when the user have more than 4500 followings
- The bot is flexible you can modify most of its features on the configuration.yml file
- You can even add links/urls to giveaways to the recent_url.txt to make the giveaways of your choice to make this work you need to set the crash_or_true on the configuration.yml to True ,search giveaways on twitter, copy and paste giveaways tweets urls to the recent_url.txt file, and the bot will do the giveaways you added

## Configuration file
The most important features can be adjust on the configuration.yml file

To add account just fill account_username and account_password with the username and password of the account you want to add

```yml
#Account info write the username of all your account
account_username:
  - "test1234"
  - "test4444"
  - "test0000"

#Account info write the password of all your account
account_password:
  - "twitter1234"
  - "twitter4444"
  - "twitter0000"
```
When the bot need to @ account you can add any account you want by adding them to the account to tag 3 accounts is enough but you can add more if you want

```yml
# Accounts we want to invite you must but a space at the end of each account
accounts_to_tag:
  - "@accoount_to_tag1 "
  - "@accoount_to_tag2 "
  - "@accoount_to_tag3 "
```

If you don't want to do giveaways of a certain account just have to add him to the accounts you want to blacklist

```yml
# Accounts that we don't want to follow and make their giveaway
accounts_to_blacklist:
  - "@account1"
  - "@account2"
  - "@account3"
```

If you don't want to do giveaway about a certain "topic" just add the "topic" to the giveaway to blacklist

```yml
# We don't want to participate in giveaway with these words
giveaway_to_blacklist:
  - "crypto"
  - "bitcoin"
  - "nft"
```
If you want to run the bot forever just set the forever_loop to true

```yml
#If forever_loop is set to true the bot will run forever otherwise it will run once
forever_loop: True
```

If the bot crashed during the run or you just want to redo the same giveaways for another account just set the crash_or_no to True and the bot will do the giveaway from the recent_url.txt file and not new giveaways

```yml
#If the bot crashed and you want to redo the giveaway you where doing just set the value to true
crash_or_no: True
```

If you don't want to do random tweet and retweet just set random_retweet_and_tweet to False but if you do want to do them just set the value to True and put the number of reetweet and tweet you want to do

```yml
# If the value is set to true the bot will make random retweet and tweet
random_retweet_and_tweet: True

# The number of random tweet to do (to make this work only if your account is new otherwise you can skip it you need to make a tweet and accept twitter circle once and then it will work)
random_tweet_nb: 10

# The number of random retweet to do
random_retweet_nb: 1
```
You can also add your own flux rss from this link https://github.com/plenaryapp/awesome-rss-feeds
```yml
#Add your own flux rss those will be used to make tweet after doing giveaway
flux_rss:
  - "https://www.france24.com/fr/rss"
```

You can also specify the number of giveaways you want to do, the number of like and retweet the giveaway must have and the limit date of a giveaway to not participate on older and finished giveaway

```yml
# Minimum of like the tweet must have
minimum_like: 10

# Minimum of reetweet the tweet must have
minimum_rt: 500

#Maximum day for a giveaway to be done
maximum_day: 14

#Number of giveaway the bot can do
nb_of_giveaway: 50
```

They are more information on the configuration.yml file but they are more easy to understand.


If you are not a french speaker or you want to do english spanish or any language giveaways read this otherwise skip it.

If you set your configuration.yml well you will be able to do giveaways that are not necessarily french just do it like that:

for the exemple let's say you want to do english giveaways

Change the tweet_lang to en or any It will either search for english tweet only or tweet of any language

```yml
# The language of the tweet to search fr,en etc put any if you want to search tweet in any language
tweet_lang: "en"
```

After that add your own word to the words_to_search list like this it will search giveaways which contain those words

```yml
# Words to search for giveaway
words_to_search:
  - "giveaway"
  - "win"
  - "contest"

```

Then you just need to modify the comment/tag list

On this list add the words that are asked when you need to comment a certain thing like if giveaways often ask "comments Done or comments #Winner" then add the word comments to the list 
```yml
# Those are the words needed on the tweet for the bot to comment when the tweet ask to comment one thing in particular
word_list_to_check_for_special_comment:
  - "comments"
```

```yml
On this list add the same word as word_list_to_check_for_special_comment but only add words that will be skip if the bot need to check for a random comment

# Those are the word needed on the tweet for the bot to comment but we won't lookup for a random comment to copy for those words:
word_list_to_not_check_for_copy:
  - "+ #"
  - "with #"
  - "add #"
````yml
On this list add the word that are asked when you need to comment on the giveaway but not necessarily anything special like if the giveaway says "comments to enter the giveaway" then add the words comments to the list

```yml
# Those are the word needed on the tweet for the bot to comment when the tweet ask to comment random stuff
word_list_to_check_for_comment:
  - "comment"
```

This list do the same things that word_list_to_check_for_comment but for word shorter than 6 characters

```yml
# The same as word_list_to_check_for_comment but for word shorter than 6 characters
short_word_list_to_check_for_comment:
  - "say"
  - "tell"
```

On this list add the word that are asked when you need to tag one or more accounts to a giveaway 
```yml
# Those are the word needed on the tweet for the bot to tag one or more account
word_list_to_check_for_tag:
  - "tag"
  - "mention"
```

Add to this list word asked when you only need to tag 1 account to enter the giveaway

```yml
# Word list to check if we need to tag 1 account
one_poeple_list:
  - "one friend"
  - "a friend"
  - "@ someone"
  
```

Add to this list word asked when you only need to tag 2 accounts to enter the giveaway

```yml
# Word list to check if we need to tag 2 accounts
two_poeple_list:
  - "two friends"
  - "two persons"
```

Add to this list word asked when you need to tag 3 or more accounts to enter the giveaway

```yml
# Word list to check if we need to tag 3 accounts or more
three_or_more_poeple_list:
  - "three friends"
  - "three persons"
  - "some friends"
```

With all of that you will be able to do giveaway in english or any language you want

## Advices  
- If you don't want to set forever_loop to True run the bot once every 2 days if you run it every day or even twice a day your account may be locked then ban
- Don't do more than 50 giveaways otherwise this could get your account locked for doing to much likes and retweets in short time

- To have the answer possible when the bot need to comment you have to add as many keywords as possible in word_list_to_check_for_special_comment,word_list_to_check_for_comment,short_word_list_to_check_for_comment list

- If you want to add other accounts to the bot you have 2 options: 
  
  1) Either add them to the configuration.yml but you won't do all the giveaways you have already done with the other accounts 
  2) Make a copy of the folder remove everything stored on the url.txt and account.txt files and store your accounts information to the configuration.yml and start the bot to make giveaways even the one your other accounts did

- If the bot crash during the run don't panic and just set the crash_or_no value to True on the configuration.yml file and restart the bot it will redo the giveaways you couldn't do because of the crash

- Don't put a min_time and max_time too low otherwise you will be locked then ban for spamming I think 45 seconds for min_time and 300 seconds for max_time is good but you can still but the time you want
- To avoid getting blocked for ban it's better to do giveaways during day time and not the night to act more human
- Fell free to modify as you wish the configuration.yml file to have the best giveaway bot you want
- Fell free to update the code or even add more features to it.

Hope this code will help you win more giveaways on twitter.
