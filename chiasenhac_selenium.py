#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import os
import random
import time

csn_mainlink = "https://chiasenhac.vn"
csn_newsongs = csn_mainlink + "/bai-hat-moi.html"
crawl_dir = "/data/user/chiasenhac/"

delay = 5 # seconds

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

# function to check duplication
def check_dup(file, directory):
    list_file = os.listdir(directory)
    if str(file) in list_file:
        return 1
    else:
        return 0

# download songs in when display main page
def download_song(driver):
    global j
    driverWait(driver)
    try:
        dl_tab = driver.find_element_by_xpath("//a[@id='pills-download-tab']")
    except NoSuchElementException:
        driver.quit()
    try:
        dl_tab.click()
    # in case the song got error, <div id="myModal" class="modal fade show"> obscures
    # press button to exit
    except ElementClickInterceptedException:
        reload_button = driver.find_element_by_xpath("//div[@class='modal_content_csn']/a")
        reload_button.click()
        return
    #  dl_text = driver.find_element_by_xpath("(//ul[@class='list-unstyled download_status']/li)[1]/a[1]")
    try:
        dl_text = driver.find_element_by_xpath("//ul[@class='list-unstyled download_status']/li[1]/a[1]")
    except NoSuchElementException:
        driver.quit()
    dl_link = dl_text.get_attribute("href")
    file_name = dl_link.split("/")[-1].replace("%20", " ")
    if not check_dup(file_name, crawl_dir):
        j += 1
        # better formatted output
        print("%6d : %s" % (j, file_name))
        dl_text.click()
    while not check_dup(str(file_name), crawl_dir):
        time.sleep(1)
        if check_dup(str(file_name), crawl_dir):
            break

# list of all new uploaded songs
choice = str(input("Enter a single CSN link or open newest uploaded by default: " or csn_newsongs))
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
        next_song = driver.find_element_by_xpath("//ul[@class='list-unstyled list_music sug_music']/li[" + str(rd) + "]//a")
        next_song.click()
    except NoSuchElementException:
        driver.quit()
    except ElementClickInterceptedException:
        reload_button = driver.find_element_by_xpath("//div[@class='modal_content_csn']/a")
        reload_button.click()
        continue
    download_song(driver)

driver.quit()


# TODO:
# check if webpage is fully loaded (DONE, really easy)
# check if files are downloaded (DONE) - using sleep and check file duplication function
# check duplicated files (DONE)
