# pylint: disable=all

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path

import pickle
from selenium.webdriver.common.action_chains import ActionChains

from search import search_tweet_for_better_rt ,  get_giveaway_url
from selenium.webdriver.common.by import By
from get_tweet import *
import traceback
import pyautogui
import feedparser
from random import randint

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

with open("configuration.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    
MINTIME = data["min_time"]
MAXTIME = data["max_time"]

uc.Chrome.__del__ = lambda self: None

class ScraperCookie:
    
    wait_time = 5
    #headless = data["headless"]
    #options = webdriver.ChromeOptions()
    options = uc.ChromeOptions()
    options.add_argument('--incognito')

    options.add_argument("--log-level=3")  # Suppress all logging levels
    
    driver = uc.Chrome(options=options)  # to open the
    time.sleep(5)
    pyautogui.hotkey('alt', 'tab')  # Passe à la fenêtre suivante (souvent Chrome)
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'tab')  # Reviens dessus pour s'assurer qu’elle est focus

    #driver = webdriver.Chrome(options=options)  # to open the chromedriver    
    #options = webdriver.FirefoxOptions()
    #options.headless = False

    #driver = webdriver.Firefox(options=options)

    username_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
    
    button_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div'
    password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_button_xpath = '/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div'
    test_tweet = 'https://x.com/Twitter/status/1580661436132757506'
    like_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[3]/div'
    cookie_button_xpath = '/html/body/div[1]/div/div/div[1]/div[1]/div/div/div/div/div[2]/button[1]/div'
    notification_button_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span/span'
    reetweet_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[2]/div'
    reetweet_confirm_button_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[2]/div/span'
    comment_button_xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/div[1]/article/div/div/div/div[3]/div[7]/div/div[1]/div'
    textbox_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
    follow_button_xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div"
    unfollow_nbr = 0

def login(S,_username,_password,reloging=False):

    try:
        try:
            S.driver.get("https://x.com/i/flow/login")
        except:
            S.driver.get("https://x.com/i/flow/login")
            time.sleep(5)
            S.driver.refresh()
            time.sleep(15)
        if reloging:
            S.driver.get("https://x.com/i/flow/login")
            time.sleep(5)
            S.driver.refresh()
            time.sleep(15)
        #USERNAME
        time.sleep(3)
        S.driver.refresh()
        time.sleep(5)
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.username_xpath)))

        username = S.driver.find_element(By.XPATH,S.username_xpath)
        for u in _username:
            time.sleep(0.3)
            username.send_keys(u)
        
        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.button_xpath)))


        #FIRST BUTTON

        button = S.driver.find_element(By.XPATH,S.button_xpath)
        button.click()


        #PASSWORD

        element = WebDriverWait(S.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, S.password_xpath)))
        
        password = S.driver.find_element(By.XPATH,S.password_xpath)
        
        for p in _password:
            password.send_keys(p)
            time.sleep(0.3)
        # print("password done")


        #LOGIN BUTTON

        element = WebDriverWait(S.driver,5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]')))
        
        login_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]')
        login_button.click()
        return True
        #print("Closing Twitter")
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            time.sleep(60*20)
            login(S,_username,_password)
        time.sleep(5)
        import traceback
        traceback.print_exc()

        for i in range(3):
            time.sleep(5)
            if check_login_good(S) == True:
                return True
        
        return False

def check_login_good(selenium_session):
    try:
        selenium_session.driver.get("https://x.com/home")
        element = WebDriverWait(selenium_session.driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Notifications_Link"]')))
        return True
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            time.sleep(60*20)
            check_login_good(selenium_session)        
        return False

def write_into_file(path, x):
    with open(path, "ab") as f:
        f.write(str(x).encode("utf-8"))

def print_pkl_info(nb):
    try:
        file_path = rf"cookies_folder\cookies{nb}.pkl"
        with open(file_path, 'rb') as file:
            try:
                data = pickle.load(file)
            except:
                return ""
        return (data)
    except Exception as e:
        if "No such file or directory" in str(e):
            write_into_file(rf"cookies_folder\cookies{nb}.pkl","")
        return ("")

def accept_coockie(S):
    try:
        S.driver.get(S.test_tweet)

        element = WebDriverWait(S.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, S.cookie_button_xpath)))
        
        cookie_button = S.driver.find_element(By.XPATH,S.cookie_button_xpath)
        cookie_button.click()

    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            time.sleep(60*20)
            accept_coockie(S)
        pass    
    
    

def check_if_good_account_login(S,account):
    try:
        S.driver.get("https://x.com/"+account)
        element = WebDriverWait(S.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'[data-testid="editProfileButton"]')))
        return False
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            time.sleep(60*20)
            check_if_good_account_login(S,account)
        return True

def save_coockie(selenium_session,nb):
    pickle.dump(selenium_session.driver.get_cookies(), open(rf"cookies_folder\cookies{nb}.pkl", "wb"))

def get_and_save_cookie(username,password,index):
    giveaway_done = 0
    with open("configuration.yml", "r",encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    
    username_info = data["account_username"]
    account_num = 0
    username_info = [username]

    for i in range(len(username_info)):
        account_num+=1
        time.sleep(1)
        S = ScraperCookie()
        ck = print_pkl_info(index)
        if len(str(ck)) > 30:
            print(f"Cookies already saved for {username}")
            S.driver.quit()
            return True
        else:
            print(f"Need to save cookies for {username}")
        
        if login(S,username,password) == False:
            time.sleep(10)
            if login(S,username,password) == False:
                S.driver.quit()
                return False
        time.sleep(60)
        if check_login_good(S) == False:
            print(f"The account is locked or password of {username} is wrong change it on the configuration.yml file")
            return False
        accept_coockie(S)
        time.sleep(S.wait_time)    
        accept_coockie(S)
        time.sleep(S.wait_time)
        
        if check_if_good_account_login(S,username):
            return False

        save_coockie(S,index)
        time.sleep(10)
        S.driver.quit()
        return True