#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# list of all new uploaded songs
driver.get(csn_newsongs)
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
  dl_tab = driver.find_element_by_xpath("//a[@id='pills-download-tab']")
  dl_tab.click()
  dl_text = driver.find_element_by_xpath("(//ul[@class='list-unstyled download_status']/li)[1]/a")
  dl_link = dl_text.get_attribute("href")
  file_name = dl_link.split("/")[-1].replace("%20", " ")
  if not check_dup(file_name, crawl_dir):
    j += 1
    print(j)
    dl_text.click()
  while not check_dup(str(file_name), crawl_dir):
    time.sleep(1)
    if check_dup(str(file_name), crawl_dir):
      break

driverWait(driver)

# get first song
first_songs = driver.find_element_by_xpath("//ul[@class='list-unstyled list_music'][1]//h5/a")
first_songs.click()

# get number of songs for download
i = int(input("Number of new songs you want to download (Default: 50): ") or "50")

# loop until exceed number of songs
j = 0
while j<i:
  # get the suggested songs from their website for our use later
  time.sleep(random.randint(1,5))
  a = random.randint(1,6)
  next_song = driver.find_element_by_xpath("(//ul[@class='list-unstyled list_music sug_music']/li)[" + str(a) + "]//a")
  next_song.click()
  download_song(driver)

driver.quit()


# TODO:
# check if webpage is fully loaded (DONE, really easy)
# check if files are downloaded (DONE) - using sleep and check file duplication function
# check duplicated files (DONE)
