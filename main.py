from twiiiiter import *
import traceback

if __name__ == "__main__":
    try:
        print("Hello world")
        with open("configuration.yml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        choice = data["main_mode"]
        if choice[0] == 1:
            main_one()
        elif choice[0] == 2:
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