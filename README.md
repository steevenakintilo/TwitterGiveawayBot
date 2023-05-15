
# TwitterGiveawayBot

Bot greatly inspired by this one: https://github.com/j4rj4r/BotTwitter

## Requirements
To make the code work you will need to have Python and Pip installed in your computer

Link to download python: https://www.python.org/downloads/

Link to download pip: https://pip.pypa.io/en/stable/installation/

Download all the modules required for the bot to work using this command:

```bash
    pip install -r requirement.txt
```

To start the bot just do

```bash
    python main.py
```

## Features

- Unlilke the other bots you can find on github this one don't use api which means that any twitter account you have can be used with this bot
- The bot work with 3 txt files: account.txt url.txt and recent_url.txt , account.txt file list all the account you have followed since using the bot, url.txt file list all the giweaway (their links) you have done sice using the bot and recent_url.txt file list all the giweaway (their links) you have done on the last time you used the bot
- Like Retweet and Comment a tweet link to a giveaway
- Follow all the person asked for the giveaway
- It can @ people when needed, comment with # when needed and make no comment when we don't need to
- The bot can do random tweet and retweet to act more "human"
- The bot can work with 1,2,20 or even 100 account you just have to fill the configuration.yml file well
- The bot is flexible you can modify most of its features on the configuration.yml file
- You can even add links to giveaways to the recent_url.txt to make this work you need to make sure the giveaways you are adding have a certain number of like retweet and good limit date all link to the configuration.yml settings and the bot will do the giveaway

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
When the bot need to @ account you can add any account you want by adding them to the account to tag 3 accounts is enough

```yml
# Accounts we want to invite you must but a space at the end of each account and a space at the start of the first account
accounts_to_tag:
  - " @accoount_to_tag1 "
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

If the bot crashed during the run or you just want to redo the same giveaways for another account just set the crash_or_no to True and the bot will do the giveaway from the recent_url.txt file and not new giveaways

```yml
#If the bot crashed and you want to redo the giveaway you where doing just set the value to true
crash_or_no: False
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
## Advices

- Run the bot once every 2 days if you run it every day or even twice a day your account may be locked then ban
- Don't do more than 50 giveaways per session otherwise you will probably reach twitter daily limits for tweet comment like retweet and follow
- If you want to add another account to the bot you have 2 options: 
  
  1) Either add it to the configuration.yml but you won't do all the giveaways you  have already done with the other account 
  2) Make a copy of the folder remove everything stored on the url.txt recent_url.txt and account.txt files and store your account information to the configuration.yml and start the bot to make giveaways even the one your other accounts did

- If the bot crash during the run don't panic and just set the crash_or_no value to True on the configuration.yml file and restart the bot it will redo the giveaways you couldn't do because of the crash

- Don't put a min_time and max_time to low otherwise you will be locked then ban for spamming I think 45 seconds for min_time and 300 seconds for max_time is good but you can still but the time you want
- Fell free to modify as you wish the configuration.yml file to have the best giveaway bot you wantFell free to update the code or even add more features to it.

Hope this code will help you win more giveaways on twitter.
