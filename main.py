from twiiiiter import *
import traceback

if __name__ == "__main__":
    try:
        print("Hello world")
        main_one()
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())