import traceback
from os import system
import yaml
import time


if __name__ == "__main__":
    index = 0
    try:
        with open("configuration.yml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        for username,password in zip(data["account_username"],data["account_password"]):
            if index == 0:
                system(f"python launch.py {username} {password} {False} {index}")
            else:
                system(f"python launch.py {username} {password} {True} {index}")
            index+=1
            time.sleep(10)
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())