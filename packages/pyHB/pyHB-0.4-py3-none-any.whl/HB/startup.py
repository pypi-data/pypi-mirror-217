import os
import time
import sys
def bot_start():
    os.system("clear")
    ask = input("Do You Want to Start HackBot y/n: ")
    if ask.lower() == "y":
        os.system("python3 -m HackBot")
    elif ask.lower() == "n":
        print("\nOk! You Can Start It Later With by using; python3-m HackBot\n")
        sys.exit()
    else:
        os.system("clear")
        print("\nInput Must Be y or n")
        bot_start()


def check_again():
    recheck = input(f"\nHave You Filled ALL Vars Correctly?: y/n: ")
    if recheck.lower() == "n":
        os.system("clear")
        print(f"Ohh! Now Fill Your Vars Again")
        LegendStartUP()
    elif recheck.lower() == "y":
        bot_start()
    else:
        print(f"\nInput Must Be Y or N")
        check_again()


def LegendStartUP():
    app_id = input(f"Enter APP_ID: ")
    if app_id:
        print(f"Got it! Fill next value")
        os.system(f"dotenv set API_ID {app_id}")
    else:
        print(f"You have to fill this variable! all process restarting..")
        time.sleep(2)
        LegendStartUP()
    api_hash = input(f"\nEnter API_HASH: ")
    if api_hash:
        print(f"Got it! Fill next value")
        os.system(f"dotenv set API_HASH {api_hash}")
    else:
        print(f"You have to fill this variable! all process restarting..")
        time.sleep(2)
        LegendStartUP()
    BOT_TOKEN = input(f"\n bot token of BOT TOKEN: ")
    if BOT_TOKEN:
        print(f"Got it! Fill next value")
        os.system(f"dotenv set BOT_TOKEN {BOT_TOKEN}")
    else:
        print(f"You have to fill this variable! all process restarting..")
        time.sleep(2)
        LegendStartUP()
    check_again()
