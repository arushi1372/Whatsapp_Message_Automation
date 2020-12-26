#!/usr/bin/env python3

"""

Sends messages to individual users using whatsapp api.
Argument is csv with columns users, messages, images, attachments.

"""

import sys
import os
import shutil
import subprocess
import logging
import math

try:
    import selenium
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    import selenium

try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import time
import datetime
import argparse
import pickle
from random import randint

def create(chrome_path):
    global wait, browser
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    try:
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    except:
        shutil.rmtree("User_Data", ignore_errors = True)
        chrome_options = Options()
        chrome_options.add_argument('--user-data-dir=./User_Data')
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
#     browser.implicitly_wait(100)
    
def call_api(number):
    global browser
    base_url = "https://wa.me/"
    url = base_url + number
    browser.get(url)
    time.sleep(3)
    # https://wa.me/12402054495
    wait5 = WebDriverWait(browser, 10)
    x_arg = '//*[@id="action-button"]'
    continue_chat = wait5.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    continue_chat.click()
    time.sleep(3)
    # continue to chat xpath: //*[@id="action-button"]
    y_arg = '//*[@id="fallback_block"]/div/div/a'
    use_web = wait5.until(EC.presence_of_element_located((By.XPATH, y_arg)))
    use_web.click()
    # use whatsapp web xpath: //*[@id="fallback_block"]/div/div/a
    whatsapp_login()
    time.sleep(10)
    
def whatsapp_login():
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except (OSError, IOError) as e:
        pickle.dump(browser.get_cookies(), open("cookies.pkl","wb"))
    browser.maximize_window()
    print("QR scanned")

def send_files(image, filename):
    global browser
    if filename is not None:
        # click on paper clip
        browser.find_element_by_css_selector("span[data-icon='clip']").click();
        filepath = os.path.join(os.getcwd(), "Files", filename)
        # click on documents button
        file_box = browser.find_element_by_xpath('//input[@accept="*"]')
        file_box.send_keys(filepath)
        time.sleep(3)
        # send
        send_button = browser.find_element_by_xpath('//span[@data-icon="send"]')
        send_button.click()
    time.sleep(3)
    if image is not None:
        browser.find_element_by_css_selector("span[data-icon='clip']").click();
        imagepath = os.path.join(os.getcwd(), "Images", image)
        image_box = browser.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        image_box.send_keys(imagepath)
        time.sleep(3)
        send_button = browser.find_element_by_xpath('//span[@data-icon="send"]')
        send_button.click()

def send_message(target, message, image = None, file = None):
    global wait, browser
    call_api(target)
    try:
        time.sleep(2)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent to: ", target)
        time.sleep(1)
        if file is not None or image is not None:
            send_files(image, file)
    except NoSuchElementException:
        with open("user_errors.txt", "a+") as f:
            print("User " + target + " not available.", file = f)
        return

def sender(user_file):
    to_send = pd.read_csv(user_file)
    to_send = to_send.fillna('')
    for index, row in to_send.iterrows():
        user = str(row["users"])
        message_file = row["messages"]
        if row['images'] == '': image = None
        else: image = row["images"]
        if row["attachments"] == '':
            file = None
        else: file = row["attachments"]
        if os.path.isfile(os.path.join("Messages", message_file)):
            with open(os.path.join("Messages", message_file), "r", encoding = "utf8") as f:
                message = f.read()
        else:
            with open(os.path.join("Messages/default.txt"), "r", encoding = "utf8") as f:
                message = f.read()
        send_message(user, message, image, file)
        time.sleep(randint(5,15))

def validate():
    return os.path.isfile("Messages/default.txt")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        user_file = sys.argv[1]
    else:
        print("Please use name of csv file containing phone numbers as an argument.")
        exit()

    sys.stderr = open('error_logs.txt', 'w')
    with open("user_errors.txt", 'w') as f:
        pass

    parser = argparse.ArgumentParser(description='Whatsapp Webdriver')
    default_path = os.path.join(os.getcwd(), 'chromedriver')
    parser.add_argument('--chrome_driver_path', action='store', type=str, default=default_path, \
                        help='chromedriver executable path (MAC and Windows path would be different)')
    parser.add_argument('--remove_cache', action='store', type=str, default='False', help='Remove Cache | Scan QR again or Not')
    parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
    args, unknown = parser.parse_known_args()

    if args.remove_cache == 'True':
        os.system('rm -rf User_Data/*')
    browser = None
    message = None if args.message == '' else args.message
    wait = None

    if not validate():
        print("Default message file located in 'Messages/default.txt' does not exist.")
        exit()

    create(args.chrome_driver_path)

    sender(user_file)

    print("Task Completed")
#     os.system("rm -rf User_Data")
    message = None
    browser.quit()