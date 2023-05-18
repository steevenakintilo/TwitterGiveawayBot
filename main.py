from twiiiiter import *
import traceback

if __name__ == "__main__":
    try:
        with open("configuration.yml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        forever_looop = data["forever_loop"]
        print("Hello world")
        if forever_looop == True:
            forever_loop()
        else:    
            main_one()
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())