
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import tweepy
import pickle

from selenium.webdriver.common.by import By

class Scraper:
    options = webdriver.ChromeOptions()
    options.add_argument(r"remote-debugging-port=9222");
    #options.add_argument('headless')
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)  # to open the chromedriver    
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

def write_into_file(path,x):  
    f = open(path, "w")
    f.write(str(x))    
    f.close            

def print_file_info(path):
    f = open(path, 'r')
    content = f.read()
    return(content)
    f.close()

def login(S,_username,_password):

    S.driver.get("https://twitter.com/i/flow/login")
    print("Starting Twitter")

    #USERNAME
    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.username_xpath)))

    username = S.driver.find_element(By.XPATH,S.username_xpath)
    username.send_keys(_username)    
    
    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.button_xpath)))


    #FIRST BUTTON

    button = S.driver.find_element(By.XPATH,S.button_xpath)
    button.click()
    print("button click")


    #PASSWORD

    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.password_xpath)))
    
    password = S.driver.find_element(By.XPATH,S.password_xpath)
    password.send_keys(_password)
    print("password done")


    #LOGIN BUTTON

    element = WebDriverWait(S.driver, 10).until(
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
    print("notification done")
    
    
def like_a_tweet(S):
    S.driver.get(S.test_tweet)
    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.like_button_xpath)))
    
    like_button = S.driver.find_element(By.XPATH,S.like_button_xpath)
    #time.sleep(1000)
    # check the "aria-pressed" attribute
    if like_button.get_attribute("aria-label") != "Aimer":
        print("You have liked the tweet.")
        return False
    else:
        like_button.click()
        print("You have not liked the tweet yet.")
        return True

def reetweet_a_tweet(S):
    S.driver.get(S.test_tweet)
    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.reetweet_button_xpath)))
    
    reetweet_button = S.driver.find_element(By.XPATH,S.reetweet_button_xpath)
    reetweet_button.click()

    element = WebDriverWait(S.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, S.reetweet_confirm_button_xpath)))
    
    reetweet_button = S.driver.find_element(By.XPATH,S.reetweet_confirm_button_xpath)
    reetweet_button.click()
    
    print("reetweet done")

    time.sleep(100)

def main():
    S = Scraper()
    login(S,"un_twittos_bleu","steeven1")
    time.sleep(3)
    accept_coockie(S)
    time.sleep(3)
    accept_notification(S)
    time.sleep(3)
    like_a_tweet(S)
    time.sleep(3)
    reetweet_a_tweet(S)

main()
