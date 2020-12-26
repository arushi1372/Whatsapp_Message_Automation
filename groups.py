#!/usr/bin/env python3

"""

Prints names of all groups in whatsapp web left pane to a txt file.

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

def whatsapp_login(chrome_path):
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    try:
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    except:
        shutil.rmtree("User_Data", ignore_errors = True)
        chrome_options = Options()
        chrome_options.add_argument('--user-data-dir=./User_Data')
        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 1000)
    browser.get(Link)
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except (OSError, IOError) as e:
        pickle.dump(browser.get_cookies(), open("cookies.pkl","wb"))
    browser.maximize_window()
    print("QR scanned")
    
def find_name():
    elem = browser.switch_to_active_element()
    html_text = str(elem.get_attribute('innerHTML'))
    first = html_text.split('<span dir="auto" title="')
    name = first[1].split('"')[0]
    return name
    
def getgroups():
    all_names = set()
    wait5 = WebDriverWait(browser, 10)
    x_arg = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    inputSearchBox = wait5.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    inputSearchBox.click()
    inputSearchBox.send_keys(Keys.ARROW_DOWN)
    name = find_name()
    all_names.add(name)
    for i in range(2000):
        actions = ActionChains(browser)
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        name = find_name()
        all_names.add(name)
     
    with open('group_names.txt', 'w') as f:
        for item in all_names:
            f.write("%s\n" % item)

if __name__ == "__main__":
    sys.stderr = open('error_logs.txt', 'w')
    with open("group_errors.txt", 'w') as f:
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
    Link = "https://web.whatsapp.com/"
    wait = None

    print("Web Page Open")

    # Login and Scan
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login(args.chrome_driver_path)
    time.sleep(10)
    
    getgroups()

    print("Task Completed")
#     os.system("rm -rf User_Data")
    message = None
    browser.quit()
