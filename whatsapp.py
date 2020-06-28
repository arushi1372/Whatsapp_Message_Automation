#!/usr/bin/env python3

import sys
import os
import shutil
import subprocess

if 'schedule' not in sys.modules:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
if 'selenium' not in sys.modules:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time
import datetime
import argparse
import pickle

parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
parser.add_argument('--chrome_driver_path', action='store', type=str, default='/Users/arushi/Desktop/PyWhatsapp-master/chromedriver', \
                    help='chromedriver executable path (MAC and Windows path would be different)')
parser.add_argument('--remove_cache', action='store', type=str, default='False', help='Remove Cache | Scan QR again or Not')
parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
args, unknown = parser.parse_known_args()

if args.remove_cache == 'True':
    os.system('rm -rf User_Data/*')
browser = None
message = None if args.message == '' else args.message
Link = "https://web.whatsapp.com/"
wait = None

def enter_new_groups(message):
    data = {}
    print("Tell us the groups you want to send messages to. Enter all groups separated by a comma.\n")
    group = str(input("Enter group names here: "))
    group = '"' + group + '"'
    group_list = group.split(",")
    for elem in group_list:
        data[elem] = message
    return data

def input_contacts():
    #if no contacts list exists, create one
    message = "ଆସନ୍ତାକାଲି ର ବିଷୟ : ଇତିହାସ – 'ଭାରତୀୟ ଜାତୀୟ ଆନ୍ଦୋଳନରେ ଗାନ୍ଧିଜୀଙ୍କ ଆବିର୍ଭାବ' \n\n" + "ସମୟ : ଘ୧୧.୦୦ \n\n" + \
"ଲାଇଭ କ୍ଲାସ୍‍ ଆସନ୍ତାକାଲି ସକାଳ ୧୧.୦୦ ଘଟିକା ସମୟରେ ଆରମ୍ଭ ହେବ । କ୍ଲାସ୍‍ ଆରମ୍ଭ ର କିଛି ସମୟ ପୁର୍ବରୁ ଆପଣଙ୍କୁ ଭିଡ଼ିଓ ର ଲିଙ୍କ୍ ଏହି Groupରେ ଦିଆଯିବ ।ଆପଣ ମାନେ ଦିଆଯାଇଥିବା ଲିଙ୍କ୍ ରେ କ୍ଲିକ୍ କରି କ୍ଲାସ୍‌ରେ ଯୋଗଦେବାକୁ ଅନୁରୋଧ । \n\n" + \
"https://youtu.be/IUHwxd0zo0A \n\n" + "ଲାଇଭ୍‍ କ୍ଲାସ୍ ଚାଲୁଅଛି । ଦୟାକରି ଉପରୋକ୍ତ ଲିଙ୍କ୍‌ରେ କ୍ଲିକ୍ କରି ଯୋଗ ଦିଅନ୍ତୁ \n"
    
    inp = str(input("Use the groups you entered last (type a) or enter new groups (type b)? (a/b)"))
    if inp == "a":
        try:
            data = pickle.load(open("groups.pkl", "rb")) 
        except (OSError, IOError) as e:
            print("No previous groups found; please enter new groups.")
            data = enter_new_groups(message)
    elif inp == "b":
        data = enter_new_groups(message)
    else:
        print("Please enter either a or b.")
        
#     try:
#         groups = pickle.load(open("groups.pkl", "rb")) 
#     except (OSError, IOError) as e:
#         print("Tell us the groups you want to send messages to. Enter all groups separated by a comma.\n")
#         while True:
#             inp = str(input("Would you like to enter another group and message? (y/n)"))
#             if inp == "y":
#                 group = str(input("Enter group name here: "))
#                 group = '"' + group + '"'
                
#                 data[group] = message
#             elif inp == "n":
#                 print(data)
#                 break
#             else:
#                 print("Please enter either y or n.")
    pickle.dump(data, open("groups.pkl","wb"))
    input("\nPress ENTER to continue...")

def input_message():
    print()
    print("Enter the message to send to this group and use the symbol '~' to end the message:\n \
    For example: Hi, this is a test message~\n\nYour message: ")
    message = ""
    temp = ""
    done = False

    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "~":
            done = True
            message += (temp[:-1])
        else:
            message += (temp)
    message = "\n".join(message)
    print()
    return message

def whatsapp_login(chrome_path):
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    try:
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    except:
        shutil.rmtree("User_Data")
        chrome_options = Options()
        chrome_options.add_argument('--user-data-dir=./User_Data')
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except (OSError, IOError) as e:
        pickle.dump(browser.get_cookies(), open("cookies.pkl","wb"))
    browser.maximize_window()
    print("QR scanned")

def send_message(target, message):
    global wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 10:
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except:
                ct += 1
                time.sleep(3)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfuly")
        time.sleep(1)
    except NoSuchElementException:
        return

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def sender():
    groups = pickle.load(open("groups.pkl", "rb"))
    for key, value in groups.items():
        group = key
        message = value
        send_message(group, message)
        print("Message sent to ", key)
    time.sleep(5)

# # Example Schedule for a particular day of week Monday
# schedule.every().monday.at("08:00").do(sender)

if __name__ == "__main__":
    print("Web Page Open")
    # Append more contact as input to send messages
    input_contacts()

    isSchedule = input('Do you want to schedule your Message(yes/no):')
    if(isSchedule == "yes"):
        jobtime = input('input time in 24 hour (HH:MM) format - ')

    # Let us login and Scan
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login(args.chrome_driver_path)
        
    if(isSchedule == "yes"):
        schedule.every().day.at(jobtime).do(sender)
    else:
        sender()

    # First time message sending Task Complete
    print("Task Completed")

    scheduler()
    message = None
    browser.quit()