#!/usr/bin/python
from selenium import webdriver
import os
import time
dir_path = os.path.dirname(os.path.realpath(__file__))

def is_captcha(driver):
	return 'class="g-recaptcha"' in chrome.page_source

PROXY = "127.0.0.1:8084"
print("Started browser")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
#chrome_options.add_argument("--headless")
chrome_options.add_argument("user-data-dir=selenium")

chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("https://www.t-mobile.com/cell-phone/samsung-galaxy-s10e")
while True:
	try:
		chrome.find_element_by_css_selector("a.cursor-pointer > span.ng-binding.ng-scope").click()
	except:
		time.sleep(1)
raw_input("continue ")
