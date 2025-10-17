from twiiiiter import *
import traceback
import sys

if __name__ == "__main__":
    try:
        #print(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
        main_one(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())