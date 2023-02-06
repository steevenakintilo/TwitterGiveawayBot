from twiiiiter import *
import traceback

if __name__ == "__main__":
    try:
        print("Hello world")
        choice = input("\nWrite 1 to launch giveaway if you have several account on the configuration.yml file.\nWrite 2 if you only have one account\nWrite 3 to quit\n\n:")
        if choice == "1":
            main_one()
        elif choice == "2":
            main_two()
        else:
            quit()
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())