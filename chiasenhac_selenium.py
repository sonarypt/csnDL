#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import os
import re
import random
import time
# remove accents in Unicode string later
import unidecode
from datetime import datetime

csn_mainlink = "https://chiasenhac.vn"
csn_newsongs = csn_mainlink + "/bai-hat-moi.html"
crawl_dir = "/data/user/musics/"

delay = 5 # seconds
delay_obscure = 10 # seconds

# create download dir if it does not exist
if not os.path.exists(crawl_dir):
    os.makedirs(crawl_dir)

# set options for Firefox
profile = webdriver.FirefoxProfile()
f = open("./firefox_config.csv", "r")
confs = f.read().splitlines()
for conf in confs:
    s1 = conf.split(" ")[0]
    ss2 = conf.split(" ")[1]
    try:
        s2 = int(ss2)
    except ValueError:
        if ss2 == "False":
            s2 = bool(0)
        elif ss2 == "True":
            s2 = bool(1)
        else:
            s2 = str(ss2)
    print(s1, ss2)
    profile.set_preference(s1, s2)

driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', firefox_profile=profile)

# function to wait for driver
def driverWait(driver):
    try:
        element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, r'/html/body/section[1]/div[2]'))
                )
    except:
        driver.quit()

def driverWaitObscure(driver):
    try:
        element = WebDriverWait(driver, delay_obscure).until(
                EC.presence_of_element_located((By.XPATH, r'//div[@class="modal-backdrop fade show"]'))
                )
    except:
        driver.quit()

# function to check duplication
def check_dup(file, directory):
    list_file = os.listdir(directory)
    if str(file) in list_file:
        return 1
    else:
        return 0

# remove some exception - remove Remix and Nonstop
r1 = '(-\w)*[Rr][Ee][Mm][Ii][Xx](\w)*'
r2 = '(-\w)*[Nn][Oo][Nn][Ss][Tt][Oo][Pp](\w)*'
r3 = '(-\w)*[Dd][Jj](\w)*'
rm = re.compile(r'(%s|%s|%s)' % (r1,r2,r3))
def check_exc(file_name):
    if rm.search(file_name):
        return 1
    else:
        return 0

# download songs in when display main page
def download_song(driver):
    global j
    driverWait(driver) 
    # search for backdrop obscure
    try:
        element = WebDriverWait(driver, delay_obscure).until(
                EC.presence_of_element_located((By.XPATH, r'//div[@class="modal-backdrop fade show"]'))
                )
        reload_button = driver.find_element_by_xpath("//div[@class='modal_content_csn']/a")
        reload_button.click()
        pass
    except:
        dl_tab = driver.find_element_by_xpath("//a[@id='pills-download-tab']")
    dl_tab.click()
    try:
        dl_text = driver.find_element_by_xpath("//ul[@class='list-unstyled download_status']/li[1]/a[1]")
    except NoSuchElementException:
        driver.quit()
    dl_link = dl_text.get_attribute("href")
    file_name = dl_link.split("/")[-1].replace("%20", " ")
    if not check_dup(file_name, crawl_dir) and not check_exc(file_name):
        j += 1
        # better formatted output
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        print("%6d : %-80s %s" % (j, file_name, current_time))
        dl_text.click()
        while not check_dup(str(file_name), crawl_dir):
            time.sleep(1)
            if check_dup(str(file_name), crawl_dir):
                break

# list of all new uploaded songs
choice = str(input("Enter a single CSN link or open newest uploaded by default: "))
if not choice:
    choice = csn_newsongs
driver.get(choice)
if choice == csn_newsongs:
    # get first song
    first_songs = driver.find_element_by_xpath("//ul[@class='list-unstyled list_music'][1]//h5/a")
    first_songs.click()

driverWait(driver)

# get number of songs for download
i = int(input("Number of new songs you want to download (Default: 50): ") or "50")

# loop until exceed number of songs
j = 0
download_song(driver)

while j<i:
    # get the suggested songs from their website for our use later
    driverWait(driver)
    time.sleep(random.randint(1,5))
    rd = random.randint(1,6) 
    try:
        element = WebDriverWait(driver, delay_obscure).until(
                EC.presence_of_element_located((By.XPATH, r'//div[@class="modal-backdrop fade show"]'))
                )
        reload_button = driver.find_element_by_xpath("//div[@class='modal_content_csn']/a")
        reload_button.click()
        pass
    # Handle error when website fail to load
    except WebDriverException:
        driver.refresh()
        driverWait()
    except:
        next_song = driver.find_element_by_xpath("//ul[@class='list-unstyled list_music sug_music']/li[" + str(rd) + "]//a")
        next_song.click()
    download_song(driver)

driver.quit()
